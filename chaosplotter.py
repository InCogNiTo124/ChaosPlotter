from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'fbo', 'hardware')
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '960')
Config.set('kivy', 'exit_on_escape', False)
Config.set('graphics', 'borderless', False)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.garden.graph import Graph, LinePlot as Plot
from kivy.graphics import Point, Color
from kivy.garden.tickmarker import TickMarker
from kivy.uix.slider import Slider
import itertools as it
import concurrent.futures as cf
import threading

R_COUNT = 1000
P_COUNT = 100

def iterate(population, r):
    while True:
        yield population
        population = r * population * (1 - population)
    return

def generate(population, r, maxiter):
    iterator = iterate(population, r)
    sequence = [(i, next(iterator)) for i in range(maxiter)]
    return sequence

def get_last(p, r, iter_count):
    iterator = iterate(p, r)
    last = 0
    for _ in range(iter_count):
        last = next(iterator)
    return last

class TickSlider(Slider, TickMarker):
    pass

class ChaosPlotter(Widget):
    population = NumericProperty(0.8)
    r = NumericProperty(2)
    graph = ObjectProperty(None)
    diagram = ObjectProperty(None)
    Graph() # There is a serious bug in a garden.graph library that can only be solved like this
    plot = Plot(color=(1, 0, 0, 1))
    diag_size = (0, 0)

    def update(self):
        self.graph.remove_plot(self.plot)
        self.plot.points = generate(self.population, self.r, self.graph.xmax)
        self.graph.add_plot(self.plot)
        return
    
    on_population = lambda self, a, b: self.update()
    on_r = on_population

    def start_bifurcation(self, size):
        print("SELF_DIAGSIZE", self.diag_size)
        size_x, size_y = size
        def f(self, size_x, size_y):
            with cf.ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(get_last, p/P_COUNT, 1 + 3*r/R_COUNT, self.graph.xmax): r/R_COUNT for p, r in it.product(range(1, P_COUNT), range(R_COUNT))}
                for future in cf.as_completed(futures):
                    r = futures[future]
                    p = future.result()
                    with self.diagram.canvas:
                        Color(0, 0, 0)
                        Point(points=[r*size_x, p*size_y], pointsize=0.5)

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
