import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from ui import createUI

class ChaosPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main = QWidget()
        self.setCentralWidget(self.main)
        self.main.setLayout(createUI(self))
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

    def refreshGraph(self, sender):
        self.graph.clear()
        self.graph.plot(np.linspace(-5, 5, 50), np.random.randn(50))

    def doConnections(self):
        self.population_slider.valueChanged.connect(lambda t: self.updatePopulation(self.sender()))
        self.population_slider.valueChanged.connect(lambda t: self.refreshGraph(self.sender()))
        self.r_slider.valueChanged.connect(lambda t: self.updateRfactor(self.sender()))
        return

if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    plotter = ChaosPlotter()
    plotter.show()
    qapp.exec()

