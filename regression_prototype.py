from tkinter import Tk, TOP, BOTH, Button, RIGHT, LEFT, Checkbutton, IntVar
from functools import partial
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from sklearn.linear_model import LinearRegression

class RegressionGUIPrototype(object):
    def __init__(self, d1, d2): #TODO: There is a lot of state here - can we encapsulate some of this?
        self.d1 = d1
        self.d2 = d2
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.axes = self.figure.add_subplot(111)
        self.master = Tk()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.x, self.y = self.d1, self.d2

    def run(self):
        self._pack_flip_button(self.master)
        self._pack_draw_fit_button(self.master)
        self._pack_plot(self.d1, self.d2, self.axes, self.canvas)
        self._pack_navigation(self.canvas, self.master)
        self.master.mainloop()

    def _clear_axes(self, axes):
        axes.clear()

    def _plot_on_axes(self, x, y, axes):
        axes.plot(x, y)

    def _pack_plot(self, x, y, axes, canvas):
        self._clear_axes(axes)
        self._plot_on_axes(x, y, axes)
        canvas.show()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def _pack_navigation(self, canvas, master):
        toolbar = NavigationToolbar2TkAgg(canvas, master)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

    def _pack_flip_button(self, master):
        b = Button(master, text='Flip', command=self._flip_axes_and_redraw)
        b.pack(side=RIGHT)

    def _flip_axes_and_redraw(self):
        #TODO: Too much internal state access? Could make this pure and construct a callback via partial fxn
        #TODO: But this is hard because x/y are part of state
        self.x, self.y = self.y, self.x
        self._clear_axes(self.axes)
        self._plot_on_axes(self.x, self.y, self.axes)
        self.canvas.draw()

    def _pack_draw_fit_button(self, master):
        checkbutton_var = IntVar()
        toggle_function = partial(self._toggle_draw_fit, checkbutton_var=checkbutton_var)
        b = Checkbutton(master, text='Draw Fit', command=toggle_function, variable=checkbutton_var)
        b.pack(side=RIGHT)

    def _toggle_draw_fit(self, checkbutton_var=None):
        self._clear_axes(self.axes)
        self._plot_on_axes(self.x, self.y, self.axes)
        self.canvas.draw()
        if checkbutton_var.get():
            m = LinearRegression().fit(self.x.reshape(-1, 1), self.y)
            x_plot = np.linspace(min(self.x), max(self.x), num=100).reshape(-1, 1)
            y_plot = m.predict(x_plot)
            self._plot_on_axes(x_plot, y_plot, self.axes)
            self.canvas.draw()

if __name__ == '__main__':
    t = np.arange(0.0, 3.0, 0.01)
    s = np.sin(2 * np.pi * t)
    RegressionGUIPrototype(t, s).run()

#TODO: Convert this into the full 2D visual Regression prototype in your notebook
#TODO: Add reading from CSV to complete prototype stage