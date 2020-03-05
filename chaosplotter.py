import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from ui import createUI, doConnections

class ChaosPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main = QWidget()
        self.setCentralWidget(self.main)
        self.main.setLayout(createUI(self))
        doConnections(self)
        self.r_slider.setMinimum(1)
        self.r_slider.setMaximum(4)
        return

if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    plotter = ChaosPlotter()
    plotter.show()
    qapp.exec()

