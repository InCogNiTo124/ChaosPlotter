from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QSlider, QLabel, QProgressBar


class MyQSlider(QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_min, self.my_max = 0, 1
        return

    def valueNormalized(self):
        return self.my_min + (self.value() / (self.maximum() - self.minimum()) * (self.my_max - self.my_min))

    def setInterval(self, interval_min, interval_max):
        self.my_min, self.my_max = interval_min, interval_max
        return


class Graph(FigureCanvas):
    def __init__(self, figsize):
        self.fig = Figure(figsize=figsize)
        self.axes = self.fig.add_subplot(1, 1, 1)
        self.line = None
        # not a bug per se, but a funny behavior
        # this mitigates it
        # https://github.com/matplotlib/matplotlib/issues/16777
        # self.axes.format_coord = lambda x, y: ""
        # unused due to simpler solution
        super().__init__(self.fig)
        return

    def plot(self, *args, **kwargs):
        return self.axes.plot(*args, **kwargs)

    def scatter(self, *args, **kwargs):
        return self.axes.scatter(*args, **kwargs)

    def clear(self, *args, **kwargs):
        return self.axes.clear(*args, **kwargs)

    def adjust(self, **kwargs):
        return self.fig.subplots_adjust(**kwargs)

    def indicator(self, R):
        if self.line is not None:
            self.line.remove()
        self.line = self.axes.axvline(R, c='red')
        self.draw_idle()
        return


def populateComboBoxes(self, problem_list, processor_list):
    box_cb = QHBoxLayout()
    self.functions_cb = QComboBox()
    for problem in problem_list:
        self.functions_cb.addItem(problem.equation)
    font = self.functions_cb.font()
    font.setPointSize(font.pointSize() + 10)
    self.functions_cb.setFont(font)
    box_cb.addWidget(self.functions_cb)
    box_cb.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding))
    self.graph_cb = QComboBox()
    for processor in processor_list:
        self.graph_cb.addItem(processor.equation)
    font = self.graph_cb.font()
    font.setPointSize(font.pointSize() + 10)
    self.graph_cb.setFont(font)
    box_cb.addWidget(self.graph_cb)
    return box_cb


def populateSliderGraph(self):
    box_sg = QHBoxLayout()
    self.population_slider = MyQSlider(Qt.Vertical)
    self.population_slider.setTickPosition(QSlider.TicksBothSides)
    box_sg.addWidget(self.population_slider)
    self.graph = Graph(figsize=(10, 3))
    box_sg.addWidget(self.graph)
    self.graph_tb = NavigationToolbar(self.graph, self, coordinates=False)
    self.graph_tb.setOrientation(Qt.Vertical)
    box_sg.addWidget(self.graph_tb)
    return box_sg


def populateLabels(self):
    box_labels = QHBoxLayout()
    self.population_label = QLabel("R = {}")
    self.r_label = QLabel("P = {}")
    box_labels.addWidget(self.population_label)
    box_labels.addWidget(self.r_label)
    box_labels.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding))
    return box_labels


def populatePlot(self):
    box_plot = QHBoxLayout()
    plot_box = QVBoxLayout()
    self.plot = Graph(figsize=(8, 5))
    self.r_slider = MyQSlider(Qt.Horizontal)
    plot_box.addWidget(self.r_slider)
    plot_box.addWidget(self.plot)
    self.plot_tb = NavigationToolbar(self.plot, self, coordinates=False)
    self.plot_tb.setOrientation(Qt.Vertical)
    box_plot.addLayout(plot_box)
    box_plot.addWidget(self.plot_tb)
    return box_plot


def createUI(self, problem_list, processor_list):
    box_v = QVBoxLayout(self.main)
    box_v.addLayout(populateComboBoxes(self, problem_list, processor_list))
    box_v.addLayout(populateSliderGraph(self))
    box_v.addLayout(populateLabels(self))
    box_v.addLayout(populatePlot(self))
    self.progress = QProgressBar()
    box_v.addWidget(self.progress)
    return box_v
