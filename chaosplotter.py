from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'fbo', 'hardware')
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '960')
#Config.set('kivy', 'exit_on_escape', False)
Config.set('graphics', 'borderless', False)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.garden.graph import Graph, LinePlot as Plot
from kivy.graphics import Point, Color
from kivy.graphics.vertex_instructions import GraphicException
from kivy.garden.tickmarker import TickMarker
from kivy.uix.slider import Slider
import itertools as it
import concurrent.futures as cf
import threading
import math

R_COUNT = 1000
P_COUNT = 100

def iterate(f, r, population):
    while True:
        yield population
        population = f(r, population)
    return

def generate(fun, r, population, maxiter):
    iterator = iterate(fun, r, population)
    sequence = [(i, next(iterator)) for i in range(maxiter)]
    del(iterator)
    return sequence

def get_last(function, r_factor, population, iter_count):
    iterator = iterate(function, r_factor, population)
    last = next(iterator)
    for _ in range(iter_count):
        last = next(iterator)
    return last

class TickSlider(Slider, TickMarker):
    pass

class ChaosPlotter(Widget):
    FUNCTIONS = [
        lambda r, p: r * p * (1 - p),
        lambda r, p: r * math.sin(math.pi * p),
        lambda r, p: r * (1 - math.cos(2*math.pi*p)) / 2,
        lambda r, p: r * p*p*(1-p),
        lambda r, p: r * p*(1 - p*p)]
    population = NumericProperty(0.74)
    r = NumericProperty(3.2)
    r_slider = ObjectProperty(None)
    graph = ObjectProperty(None)
    diagram = ObjectProperty(None)
    progress = ObjectProperty(None)
    function_index = NumericProperty(None)
    Graph() # There is a serious bug in a garden.graph library that can only be solved like this
    plot = Plot(color=(1, 0, 0, 1))
    diag_size = (0, 0)

    def update_r_slider(self):
        n = self.r_slider.value_normalized
        if self.function_index == 0:
            self.r_slider.min = 1
            self.r_slider.max = 4
        elif self.function_index == 1:
            self.r_slider.min = 0.5
            self.r_slider.max = 1
        elif self.function_index == 2:
            self.r_slider.min = 0.439
            self.r_slider.max = 0.879
        elif self.function_index == 3:
            self.r_slider.min = 4
            self.r_slider.max = 6.543
        elif self.function_index == 4:
            self.r_slider.min = 1
            self.r_slider.max = 3
        self.r_slider.value_normalized = n
        return

    def on_function_index(self, a, b):
        self.update_r_slider()
        self.start_bifurcation(self.diag_size, self.FUNCTIONS[self.function_index])


    def update_graph(self):
        if self.function_index is not None:
            self.graph.remove_plot(self.plot)
            self.plot.points = generate(self.FUNCTIONS[self.function_index], self.r, self.population, self.graph.xmax)
            self.graph.add_plot(self.plot)
        return
    
    on_population = lambda self, a, b: self.update_graph()
    on_r = on_population

    def start_bifurcation(self, size, function):
        self.progress.value = 0
        self.update_graph()
        #print(self.diagram.canvas.__dict__)
        self.diagram.canvas.clear()
        size_x, size_y = size
        def f(self, size_x, size_y):
            r_min = self.r_slider.min
            r_max = self.r_slider.max
            with cf.ThreadPoolExecutor(max_workers=5) as executor:
                futures = {
                    executor.submit(get_last, function, r_min + (r_max - r_min)*r/R_COUNT, p/P_COUNT, self.graph.xmax): r/R_COUNT
                    for p, r in it.product(range(1, P_COUNT), range(R_COUNT))
                }
                self.progress.max = len(futures)
                points = Point(points=[], pointsize=0.5)
                with self.diagram.canvas:
                    Color(0, 0, 0)
                self.diagram.canvas.add(points)
                for future in cf.as_completed(futures):
                    self.progress.value += 1
                    r = futures[future]
                    p = future.result()
                    #with self.diagram.canvas:
                    #    Color(0, 0, 0)
                    #    Point(points=[r*size_x, p*size_y], pointsize=0.5)
                    try:
                        points.add_point(r*size_x, p*size_y)
                    except GraphicException:
                        print("LIMIT")
                        points = Point(points=[r*size_x, p*size_y], pointsize=0.5)
                        self.diagram.canvas.add(points)

            return
        threading.Thread(target=f, args=(self,size_x, size_y)).start()
        return

class ChaosPlotterApp(App):
    def build(self):
        self.plotter = ChaosPlotter()
        return self.plotter

if __name__ == "__main__":
    a = ChaosPlotterApp()
    a.run()
