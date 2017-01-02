from tkinter import Tk, TOP, BOTH, Button, RIGHT, LEFT, Checkbutton, IntVar, Frame
from functools import partial
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from sklearn.linear_model import LinearRegression
from collections import namedtuple

class RegressionData(object):
    def __init__(self, design_matrix):
        self.design_matrix = design_matrix
        self.target_variable_index = 1

    def get_training_data(self):
        return self.design_matrix[:, 1-self.target_variable_index], self.design_matrix[:,self.target_variable_index]

    def flip(self):
        self.target_variable_index = 1 - self.target_variable_index

class RegressionGUIPrototype(object):
    def __init__(self, data_matrix): #TODO: There is a lot of state here - can we encapsulate some of this?
        self.regression_data = RegressionData(data_matrix)
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.axes = self.figure.add_subplot(111)
        self.master = Tk()
        self.left_frame = Frame(self.master)
        self.right_frame = Frame(self.master)
        self.left_frame.pack(side=LEFT)
        self.right_frame.pack(side=RIGHT)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.left_frame)

    def run(self):
        self._pack_flip_button(self.right_frame)
        self._pack_draw_fit_button(self.right_frame)
        x, y = self.regression_data.get_training_data()
        self._pack_plot(x, y, self.axes, self.canvas)
        self._pack_navigation(self.canvas, self.left_frame)
        self.master.mainloop()

    def _clear_axes(self, axes):
        axes.clear()

    def _scatter_on_axes(self, x, y, axes):
        axes.scatter(x, y, color='b')

    def _plot_on_axes(self, x, y, axes):
        axes.plot(x, y, color='r')

    def _pack_plot(self, x, y, axes, canvas):
        self._clear_axes(axes)
        self._scatter_on_axes(x, y, axes)
        canvas.show()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=TOP, fill=BOTH, expand=1)

    def _pack_navigation(self, canvas, frame):
        toolbar = NavigationToolbar2TkAgg(canvas, frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

    def _pack_flip_button(self, frame):
        b = Button(frame, text='Flip', command=self._flip_axes_and_redraw)
        b.pack()

    def _flip_axes_and_redraw(self):
        #TODO: Too much internal state access? Could make this pure and construct a callback via partial fxn
        #TODO: But this is hard because x/y are part of state
        self.regression_data.flip()
        x, y = self.regression_data.get_training_data()
        self._clear_axes(self.axes)
        self._scatter_on_axes(x, y, self.axes)
        self.canvas.draw()

    def _pack_draw_fit_button(self, master):
        checkbutton_var = IntVar()
        toggle_function = partial(self._toggle_draw_fit, checkbutton_var=checkbutton_var)
        b = Checkbutton(master, text='Draw Fit', command=toggle_function, variable=checkbutton_var)
        b.pack()

    def _toggle_draw_fit(self, checkbutton_var=None):
        self._clear_axes(self.axes)
        x, y = self.regression_data.get_training_data()
        self._scatter_on_axes(x, y, self.axes)
        self.canvas.draw()
        if checkbutton_var.get():
            m = LinearRegression().fit(x.reshape(-1, 1), y)
            x_plot = np.linspace(min(x), max(x), num=100).reshape(-1, 1)
            y_plot = m.predict(x_plot)
            self._plot_on_axes(x_plot, y_plot, self.axes)
            self.canvas.draw()

if __name__ == '__main__':
    t = np.arange(0.0, 10.0, 0.01)
    s = t*0.5 + 10 + np.random.normal(0, 1, len(t))
    data_matrix = np.array([t, s]).T
    RegressionGUIPrototype(data_matrix).run()

#TODO: Convert this into the full 2D visual Regression prototype in your notebook
#TODO: Add reading from CSV to complete prototype stage