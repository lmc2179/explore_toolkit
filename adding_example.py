from tkinter import Tk, Label, Button, Canvas, Entry, TOP, X, mainloop, LEFT, StringVar
from functools import partial

master = Tk()

e1 = Entry(master)
e1.pack()
e2 = Entry(master)
e2.pack()

value = StringVar(master)
value.set('N/A')

def callback(result_var=None):
    result_var.set(float(e1.get()) + float(e2.get()))

callback_no_args = partial(callback, result_var=value)

b = Button(master, text="Add", width=10, command=callback_no_args)
b.pack()

l = Label(master, textvariable = value)
l.pack()

mainloop()

# Goal: Stateful application - 2 texts fields, button to add them