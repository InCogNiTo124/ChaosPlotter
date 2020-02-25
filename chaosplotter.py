import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.garden.graph import Graph, LinePlot as Plot
#from kivy.uix.slider import Slider
#from kivy.uix.boxlayout import BoxLayout


ITER_COUNT = 5000
def iterate(population, r):
    while True:
        yield population
        population = r * population * (1 - population)
    return

def generate(population, r):
    iterator = iterate(population, r)
    sequence = [(i, next(iterator)) for i in range(ITER_COUNT)]
    #print(sequence)
    return sequence

class ChaosPlotter(Widget):
    population = NumericProperty(0.8)
    r = NumericProperty(2)
    graph = ObjectProperty(None)
    Graph() # There is a serious bug in a garden.graph library that can only be solved like this
    plot = Plot(color=(1, 0, 0, 1))

    def update(self):
        self.graph.remove_plot(self.plot)
        #self.plot = Plot(color=(1, 0, 0, 1))
        self.plot.points = generate(self.population, self.r)
        self.graph.add_plot(self.plot)
        return
    
    on_population = lambda self, a, b: self.update()
    on_r = on_population

class ChaosPlotterApp(App):
    def build(self):
        plotter = ChaosPlotter()
        plotter.update()
        return plotter

if __name__ == "__main__":
    ChaosPlotterApp().run()
