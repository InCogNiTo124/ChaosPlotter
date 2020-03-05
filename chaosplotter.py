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
        return

if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    plotter = ChaosPlotter()
    plotter.show()
    qapp.exec()

