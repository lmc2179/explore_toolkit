from tkinter import Tk, TOP, BOTH, Label
import datetime

master = Tk()

w = Label(master, text=str(datetime.datetime.now()))
w.pack()

def update_label():
    w.config(text=str(datetime.datetime.now()))
    master.after(1, update_label)

update_label()
master.mainloop()