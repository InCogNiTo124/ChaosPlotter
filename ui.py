import numpy as np
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (
    QWidget, QComboBox, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QSlider, QLabel
)

class MyQSlider(QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        return

    def valueNormalized(self):
        return self.value() / (self.maximum() - self.minimum())

class Graph(FigureCanvas):
    def __init__(self, figsize):
        fig = Figure(figsize=figsize)
        self.axes = fig.add_subplot(1, 1, 1)
        super().__init__(fig)
        return

    def plot(self, *args, **kwargs):
        return self.axes.plot(*args, **kwargs)

def populateComboBoxes(self):
    box_cb = QHBoxLayout()
    functions_cb = QComboBox()
    for item in ["R \u00b7 P\u2099(1 - P\u2099)", "R \u00b7 sin(P\u2099)"]:
        functions_cb.addItem(item)
    box_cb.addWidget(functions_cb)
    box_cb.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding))
    graph_cb = QComboBox()
    for item in ["P\u2099", "\u2131[P\u2099]", "P\u2099\u208A\u2081 - P\u2099", "\u2131[P\u2099\u208A\u2081 - P\u2099]"]:
        graph_cb.addItem(item)
    box_cb.addWidget(graph_cb)
    return box_cb

def populateSliderGraph(self):
    box_sg = QHBoxLayout()
    self.population_slider = MyQSlider(Qt.Vertical)
    self.population_slider.setTickPosition(QSlider.TicksBothSides)
    box_sg.addWidget(self.population_slider)
    self.graph = Graph(figsize=(10, 3))
    box_sg.addWidget(self.graph)
    return box_sg

def populateLabels(self):
    box_labels = QHBoxLayout()
    self.population_label = QLabel("R = {}")
    self.r_label = QLabel("P = {}")
    box_labels.addWidget(self.population_label)
    box_labels.addWidget(self.r_label)
    box_labels.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding))
    return box_labels

def createUI(self):
    box_v = QVBoxLayout(self.main) 
    box_v.addLayout(populateComboBoxes(self))
    box_v.addLayout(populateSliderGraph(self))
    box_v.addLayout(populateLabels(self))
    self.r_slider = MyQSlider(Qt.Horizontal)
    box_v.addWidget(self.r_slider)

    self.plot = Graph(figsize=(8, 5))
    box_v.addWidget(self.plot)
    x = np.linspace(-5, 5, 101)
    y = np.exp(-x**2)
    self.graph.plot(x, y)

    self.plot.plot(np.linspace(-10, 10, 501), np.random.randn(501))
    return box_v

def updatePopulation(self, sender):
    self.population_label.setText("P = {:.02}".format(sender.valueNormalized()))
    return

def updateRfactor(self, sender):
    self.r_label.setText("P = {:.02}".format(sender.valueNormalized()))

def doConnections(self):
    self.population_slider.valueChanged.connect(lambda t: updatePopulation(self, self.sender()))
    self.r_slider.valueChanged.connect(lambda t: updateRfactor(self, self.sender()))
    return
