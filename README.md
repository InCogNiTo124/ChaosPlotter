# ChaosPlotter
![Screenshot](/ChaosPlotterScreenshot.png)
Plot chaos using Python/Kivy
## What is it?
It's a visualization of iterated maps. A starting population P is selected (by a vertical slider on the far left) and then run through a function (as selected in the upper left). The result is then feeded once again through the same function, over and over again. This is called *map iteration*. Sequential values are plotted in the graph in the upper right.
An interesting behaviour can be observed if the value of R (big central horizontal slide) is increased. At first, almost every^(1)^ starting population converges to a fixed number. By increasing the R slider even more, our iterated map starts to oscillate between 2 values. If R keeps getting bigger, we see the period 4, than 8, 16... and so on until it gets chaotic and starts to take any value from [0, 1] interval in a seemingly random fashion.
AND THEN, if R keeps increasing, from chaos emerges order. Our wild iterated map settles down to oscillations with period of 3. And then 6. And then 12. And then more chaos^(2)^, until R hits 4, where our maps starts to diverge.
If we plot the values that he map converges to as a function of R, we get a [bifurcation diagram](https://en.wikipedia.org/wiki/Bifurcation_diagram) (the big graph at the bottom). The bifurcation is a fancy word to say "it splits in two and looks like a fork".
- ^(1)^ This is true for all values in <0, 1>, and maybe some points inside
- ^(2)^ Actually, you can find periods of any length: 5, 13, 120497... you name it, it's there somewhere

## How to use it?
1. Choose a function you wish to iterate. The first one usually gives the best results.
2. Observe the bifurcation diagram slowly appearing in front of you and be amazed.
3. Change the R with the big slider in the middle. Observe what happens with the population graph. The vertical line in the diagram shows where the population graph from above fits into the bifurcation diagram. Be more amazed.
4. Change the starting population:
	1. If you're in the "tame" zone, observe how the oscillating values don't change much with the starting population.
	2. If you're in the "chaotic" zone, observe how the small changes in the starting population appear to have a massive effect on a population dynamics. Also, try to find very different starting populations that have similar dynamics. Both exist :) and 0 and 1 don't count >:(
5. Try a new map and be amazed :D

## How to run?
I've prepared a simple bash script to get you going:
```bash
git clone https://github.com/InCogNiTo124/ChaosPlotter.git && cd ChaosPlotter
. setup
```
This script will build a virtual environment `venv`, install and initialize dependencies in it. If you wish to install dependencies globally, just call `setup` with `--no-venv`. **This is strongly discouraged**.

After setting this repo up, simply run:
```bash
python chaosplotter.py
```

