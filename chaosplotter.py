import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.garden.graph import Graph, LinePlot as Plot
#from kivy.uix.slider import Slider
#from kivy.uix.boxlayout import BoxLayout


ITER_COUNT = 10
def iterate(population, r):
    while True:
        yield population
        population = r * population * (1 - population)
    return

def generate(population, r):
    iterator = iterate(population, r)
    sequence = [(i, next(iterator)) for i in range(ITER_COUNT)]
    return sequence

class ChaosPlotter(Widget):
    population = NumericProperty(0.5)
    r = NumericProperty(2)
    graph = Graph()
    plot = Plot()

    def update(self):
        self.graph.remove_plot(self.plot)
        self.plot.points = generate(self.population, self.r)
        self.graph.add_plot(self.plot)
        return
    
    on_population = lambda self, a, b: self.update()
    on_r = on_population

class ChaosPlotterApp(App):
    def build(self):
        return ChaosPlotter()

if __name__ == "__main__":
    ChaosPlotterApp().run()
