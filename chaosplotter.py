import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout

class ChaosPlotter(Widget):
    pass

class ChaosPlotterApp(App):
    def build(self):
        return ChaosPlotter()

if __name__ == "__main__":
    ChaosPlotterApp().run()
