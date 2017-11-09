# from Tkinter import *
# import Tkinter as ttk
# from ttk import *
import tkinter
from tkinter import ttk
from tkinter import *

root = tkinter.Tk()
root.title("Select Color")

# Add a grid
colors_frame = ttk.Frame(root, padding=20, relief='raised')
colors_frame.grid()

# Create a Tkinter variable

# Dictionary with options
choices = {'Pizza', 'Lasagne', 'Fries', 'Fish', 'Potatoe'}
tkvar.set('Pizza')  # set the default option

popupMenu = ttk.OptionMenu(colors_frame, tkvar, *choices)
ttk.Label(colors_frame, text="Choose a dish").grid(row=1, column=1)
popupMenu.grid(row=2, column=1)


# on change dropdown value
def change_dropdown(*args):
    print(tkvar.get())


# link function to change dropdown
tkvar.trace('w', change_dropdown)

root.mainloop()