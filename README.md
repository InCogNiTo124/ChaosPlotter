
# ChaosPlotter
![Screenshot](/ChaosPlotterScreenshot.png)
Plot chaos using Python3/[Kivy](https://kivy.org/)
## What is it?
It's a visualization of iterated maps. A starting population P is selected (by a vertical slider on the far left) and then run through a function (as selected in the upper left). The result is then feeded once again through the same function, over and over again. This is called *MAP ITERATION*. Sequential values are plotted with the red line on the graph in the upper right.
An interesting behaviour can be observed if the value of R (big central horizontal slide) is increased. At first, almost every<sup>1</sup> starting population converges to a fixed number. By increasing the R slider even more, our iterated map starts to oscillate between 2 values. If R keeps getting bigger, we see the period 4, than 8, 16... and so on until it gets chaotic and starts to take any value from [0, 1] interval in a seemingly random fashion.
*AND THEN*, if R keeps increasing, from chaos emerges order. Our wild iterated map settles down to oscillations with period of 3. And then 6. And then 12. And then more chaos<sup>2</sup>, until R hits 4, where our maps starts to diverge.
If we plot the values the map converges to as a function of R, we get a [bifurcation diagram](https://en.wikipedia.org/wiki/Bifurcation_diagram) (the big graph at the bottom). "Bifurcation" is a fancy word to say "it splits in two and looks like a fork".

## How to use it?
1. Choose a function you wish to iterate. The first one usually gives the best results.
2. Observe the bifurcation diagram slowly<sup>3</sup> appearing in front of you and be amazed.
3. Change the R with the big slider in the middle. Observe what happens with the population graph. The vertical line in the diagram shows where the population graph from above fits into the bifurcation diagram. Be more amazed.
4. Change the starting population:
	1. If you're in the "tame" zone, observe how the oscillating values don't change much with respect to the starting population.
	2. If you're in the "chaotic" zone, observe how the small changes in the starting population appear to have a massive effect on the population dynamics. Maybe try to find very different starting populations that have similar dynamics. Both situations exist :) and 0 and 1 don't count >:(
5. Try a new map and be even more amazed :D

## How to run?
I've prepared a simple bash script to get you going:
```bash
git clone https://github.com/InCogNiTo124/ChaosPlotter.git && cd ChaosPlotter
bash setup.sh
```
This script will build a virtual environment called `venv` and install and initialize all of the dependencies in it. An obvious prerequisite is [`virtualenv`](https://virtualenv.pypa.io/). Another obvious prerequisite is `python3`.
If you dislike environments or wish to install dependencies globally, just call `setup.sh --no-venv`. **This is strongly discouraged**.

After setting this repository up, simply run:
```bash
source venv/bin/activate
python chaosplotter.py
```
and enjoy :)

- <sup>1</sup> This is true for all values in [0, 1], except 0 and 1 (so technically <0, 1>), and maybe some points inside that interval
- <sup>2</sup> Actually, you can find periods of any length: 5, 13, 120497... You name the natural number, the corresponding period is in there somewhere
- <sup>3</sup> Yes, I am aware of how slow it is. It takes, on average, around 60 seconds on my Ryzen 7
## Wish to contribute?
You are very welcome. Just open an issue or push a PR.

### TODO:
- Add more modes for population visualization:
	- [ ] Fourier transform of the population
	- [ ] Difference from the previous population
	- [ ] Fourier transform of the difference
	- [ ] Something else?!
- I wish to have a dropdown of functions to iterate rendered either in latex or [Kivy markup](https://kivy.org/doc/stable/api-kivy.core.text.markup.html)
- Speed
	- [ ] Integration with numpy
	- [ ] Better multithreading / processing

