import sys
import numpy as np
from numpy import fft
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from ui import createUI
import concurrent.futures as cf
from threading import Thread


def dft(x, norm=None):
    x = fft.fft(x, norm=norm)
    x = fft.fftshift(x)
    x = np.abs(x)
    x = np.log(x)
    return x


def iterate(function, R, P, iter_count, history=False):
    if history:
        population = [P]
    for i in range(iter_count):
        P = function(R, P)
        if history:
            population.append(P)
    return np.array(population).ravel() if history else P


class Function:
    def __init__(self, name, equation, function, limits=(0.0, 1.0)):
        self.name = name
        self.equation = equation
        self.function = function
        self.limits = limits
        return

    def __call__(self, *args):
        return self.function(*args)


class ChaosPlotter(QMainWindow):
    PROBLEMS = [
        Function("stub", "Select...", lambda r, p: p, (0, 0)),
        Function("logistic", "R \u00b7 P\u2099(1 - P\u2099)", lambda r, p: r * p * (1-p), (1, 4)),
        Function("sin", "R \u00b7 sin(P\u2099)", lambda r, p: r * np.sin(np.pi * p), (0.31, 1.0)),
        Function("triangle", "R \u00b7 \u0394(P\u2099)", lambda r, p: r * np.minimum(p, 1-p), (0.0, 2.0)),
    ]

    PROCESSORS = [
        Function("population", "P\u2099", lambda x: x, (0, 1)),
        Function("fft(pop)", "\u2131[P\u2099]", lambda x: dft(x, norm='ortho'), (-10, 4)),
        Function("diff", "P\u2099\u208A\u2081 - P\u2099", lambda x: np.diff(x), (-1, 1)),
        Function("fft(diff)", "\u2131[P\u2099\u208A\u2081 - P\u2099]",
                 lambda x: dft(np.diff(x), norm='ortho'), (-10, 4)),
    ]

    def __init__(self):
        super().__init__()
        self.main = QWidget()
        self.setCentralWidget(self.main)
        self.main.setLayout(createUI(self, self.PROBLEMS, self.PROCESSORS))
        self.r_slider.setMinimum(0)
        self.r_slider.setMaximum(10000)
        self.r_slider.setValue(5000)
        self.r_slider.setInterval(1, 4)
        self.r_slider.setEnabled(False)
        self.updateRfactor(self.r_slider)
        self.population_slider.setMinimum(0)
        self.population_slider.setMaximum(1000)
        self.population_slider.setValue(500)
        self.population_slider.setEnabled(False)
        self.updatePopulation(self.population_slider)
        self.doConnections()
        self.processor_index = 0
        self.problem_index = 0
        self.graph.adjust(left=0.02, right=0.99, top=0.975, bottom=0.075)
        return

    def updatePopulation(self, sender):
        self.population_label.setText("P = {}".format(round(sender.valueNormalized(), 2)))
        return

    def updateRfactor(self, sender):
        self.r_label.setText("R = {}".format(round(sender.valueNormalized(), 3)))
        return

    def refreshGraph(self):
        function = self.getCurrentFunction()
        P = np.array([self.population_slider.valueNormalized()])
        R = self.r_slider.valueNormalized()
        population = iterate(function, R, P, 5040, history=True)
        processor = self.getCurrentProcessor()
        y_val = processor(population)
        x_val = np.arange(0, len(y_val), 1)
        self.graph.clear()
        limits = processor.limits
        self.graph.axes.set_ylim(*limits)
        self.graph.plot(x_val, y_val, '.', markersize=4.0)
        self.graph.draw()

        self.plot.indicator(R)
        return

    def plotBifurcation(self):
        function = self.getCurrentFunction()
        r_limits = function.limits
        R_count = 110880  # refactor to settings
        # currently not supported:
        # splits > 1
        # splits is actually the number of jobs for a threadpool
        # severe bugs are present if splits is not 1
        # i literally have no idea how to fix it, bit this is fast enough
        splits = 1  # refactor to settings
        iter_count = 3000  # refactor to settings
        self.plot.clear()
        self.plot.axes.set_xlim(*r_limits)
        self.plot.axes.set_ylim(0.0, 1.0)
        self.plot.adjust(left=0.005, right=0.995, bottom=0.0, top=1.0)
        self.progress.setRange(0, splits)
        self.progress.setValue(0)
        self.progress.show()
        self.plot.indicator(self.r_slider.valueNormalized())
        Thread(target=self.makeplot, args=(self.plot, function, r_limits, R_count, splits, iter_count)).start()
        return

    def makeplot(self, plot, function, r_limits, R_count, splits, iter_count, callback=None):
        R = np.linspace(*r_limits, R_count)
        with cf.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(iterate, function, r, np.random.random(R_count // splits), iter_count, False): r
                for r in np.split(R, splits)
            }
            for future in cf.as_completed(futures):
                r = futures[future]
                p = future.result()
                plot.scatter(r, p, s=0.1, c='black')
                self.progress.setValue(self.progress.value() + 1)
                plot.draw_idle()
        return

    def handleFunctionChange(self, index):
        self.problem_index = index
        if index > 0:
            self.r_slider.setEnabled(True)
            self.population_slider.setEnabled(True)
            r_limits = self.getCurrentFunction().limits
            self.r_slider.setInterval(*r_limits)
            self.refreshGraph()
            self.plotBifurcation()
        else:
            self.r_slider.setEnabled(False)
            self.population_slider.setEnabled(False)
        return

    def handleProcessorChange(self, index):
        self.processor_index = index
        self.refreshGraph()
        return

    def doConnections(self):
        self.population_slider.valueChanged.connect(lambda t: self.updatePopulation(self.sender()))
        self.population_slider.valueChanged.connect(lambda t: self.refreshGraph())
        self.r_slider.valueChanged.connect(lambda t: self.updateRfactor(self.sender()))
        self.r_slider.valueChanged.connect(lambda t: self.refreshGraph())
        self.functions_cb.currentIndexChanged.connect(lambda t: self.handleFunctionChange(t))
        self.graph_cb.currentIndexChanged.connect(lambda t: self.handleProcessorChange(t))
        return

    def getCurrentFunction(self):
        return self.PROBLEMS[self.problem_index]

    def getCurrentProcessor(self):
        return self.PROCESSORS[self.processor_index]


if __name__ == "__main__":
    sys.argv[0] = "Chaos Plotter"
    qapp = QApplication(sys.argv)
    plotter = ChaosPlotter()
    plotter.show()
    qapp.exec()
