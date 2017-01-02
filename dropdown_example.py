from tkinter import Tk, Label, Button, Canvas, Entry, TOP, X, mainloop, LEFT, StringVar, OptionMenu
from functools import partial

master = Tk()

value = StringVar(master)
value.set('N/A')
m = OptionMenu(master, value, *[0, 1, 2])
m.pack()

def callback(result_var=None):
    print(result_var.get())

callback_no_args = partial(callback, result_var=value)

b = Button(master, text="Get Dropdown value", command=callback_no_args)
b.pack()

# l = Label(master, textvariable = value)
# l.pack()

mainloop()

# Goal: Stateful application - 2 texts fields, button to add them