import sys
import numpy as np
from numpy import fft
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from ui import createUI

def dft(x, norm=None):
    x = fft.rfft(x, norm=norm)
    x = np.abs(x)
    x = np.log(x)
    #x = fft.fftshift(x)
    return x


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
        Function("sin", "R \u00b7 sin(P\u2099)", lambda r, p: r * np.sin(np.pi * p), (0.3, 1)),
    ]
    
    PROCESSORS = [
        Function("population", "P\u2099", lambda x: x),
        Function("fft(pop)", "\u2131[P\u2099]", lambda x: dft(x, norm='ortho')),
        Function("diff", "P\u2099\u208A\u2081 - P\u2099", lambda x: np.diff(x)),
        Function("fft(diff)", "\u2131[P\u2099\u208A\u2081 - P\u2099]", lambda x: dft(np.diff(x), norm='ortho')),
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
        self.population_slider.setMinimum(0)
        self.population_slider.setMaximum(1000)
        self.population_slider.setValue(500)
        self.population_slider.setEnabled(False)
        self.doConnections()
        self.processor_index = 0
        self.problem_index = 0
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
        population = [P]
        processor = self.getCurrentProcessor()
        #print(processor.name)
        for i in range(5000):
            P = function(R, P)
            population.append(P)
        population = np.array(population).flatten()
        y_val = processor(population))
        #print(y_val.shape)
        x_val = np.arange(0, len(y_val), 1)
        #print(x_val, y_val)
        #M = max(y_val[1:])
        self.graph.clear()
        self.graph.axes.set_ylim(-10, 5)
        self.graph.plot(x_val, y_val, '.')
        self.graph.draw()
        return

    def plotBifurcation(self):
        function = self.getCurrentFunction()
        r_limits = function.limits
        p = np.random.random(10000)
        r = np.linspace(*r_limits, 10000)
        for i in range(1000):
            p = function(r, p)
        self.plot.clear()
        self.plot.scatter(r, p, s=0.1)
        self.plot.draw()
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
        #print(self.processor_index)
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
    qapp = QApplication(sys.argv)
    plotter = ChaosPlotter()
    plotter.show()
    qapp.exec()


