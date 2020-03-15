import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from ui import createUI

class Function:
    def __init__(self, name, equation, function, r_limits):
        self.name = name
        self.equation = equation
        self.function = function
        self.r_limits = r_limits
        return

    def __call__(self, r, p):
        return self.function(r, p)

class ChaosPlotter(QMainWindow):
    PROBLEMS = [
        Function("stub", "Select...", lambda r, p: p, (0, 0)),
        Function("logistic", "R \u00b7 P\u2099(1 - P\u2099)", lambda r, p: r * p * (1-p), (1, 4)),
        Function("sin", "R \u00b7 sin(P\u2099)", lambda r, p: r * np.sin(np.pi * p), (0, 2)),
    ]

    def __init__(self):
        super().__init__()
        self.main = QWidget()
        self.setCentralWidget(self.main)
        self.main.setLayout(createUI(self, self.PROBLEMS))
        self.doConnections()
        self.r_slider.setMinimum(0)
        self.r_slider.setMaximum(10000)
        self.r_slider.setInterval(1, 4)
        return

    def updatePopulation(self, sender):
        self.population_label.setText("P = {}".format(round(sender.valueNormalized(), 2)))
        return

    def updateRfactor(self, sender):
        self.r_label.setText("R = {}".format(round(sender.valueNormalized(), 3)))
        return

    def refreshGraph(self):
        P = np.array([self.population_slider.valueNormalized()])
        R = self.r_slider.valueNormalized()
        population = [P]
        for i in range(1000):
            P = self.function(R, P)
            population.append(P)
        self.graph.clear()
        self.graph.axes.set_ylim(0.0, 1.0)
        self.graph.plot(np.arange(0, len(population), 1), population, '.')
        self.graph.draw()
        return

    def handleFunctionChange(self, index):
        if index > 0:
            #print(self.function_index)
            self.function = self.PROBLEMS[index]
            self.r_slider.setInterval(*self.function.r_limits)
            self.refreshGraph()
        return

    def doConnections(self):
        self.population_slider.valueChanged.connect(lambda t: self.updatePopulation(self.sender()))
        self.population_slider.valueChanged.connect(lambda t: self.refreshGraph())
        self.r_slider.valueChanged.connect(lambda t: self.updateRfactor(self.sender()))
        self.r_slider.valueChanged.connect(lambda t: self.refreshGraph())
#        self.functions_cb.activated.connect(lambda t: self.handleFunctionChange(t))
        self.functions_cb.currentIndexChanged.connect(lambda t: self.handleFunctionChange(t))
        return

if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    plotter = ChaosPlotter()
    plotter.show()
    qapp.exec()

