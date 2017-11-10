# # from Tkinter import *
# # import Tkinter as ttk
# # from ttk import *
# import tkinter
# from tkinter import ttk
# from tkinter import *
#
# root = tkinter.Tk()
# root.title("Select Color")
#
# # Add a grid
# colors_frame = ttk.Frame(root, padding=20, relief='raised')
# colors_frame.grid()
#
# # Create a Tkinter variable
#
# # Dictionary with options
# choices = {'Pizza', 'Lasagne', 'Fries', 'Fish', 'Potatoe'}
# tkvar.set('Pizza')  # set the default option
#
# popupMenu = ttk.OptionMenu(colors_frame, tkvar, *choices)
# ttk.Label(colors_frame, text="Choose a dish").grid(row=1, column=1)
# popupMenu.grid(row=2, column=1)
#
#
# # on change dropdown value
# def change_dropdown(*args):
#     print(tkvar.get())
#
#
# # link function to change dropdown
# tkvar.trace('w', change_dropdown)
#
# root.mainloop()

def color_to_look_for_red(self):
    self.pixy.mode = "SIG1"
    turn_speed = 100

    while not self.touch_sensor.is_pressed:

        print("value1: X", self.pixy.value(1))
        print("value2: Y", self.pixy.value(2))

        if self.pixy.value(1) < 150:
            self.drive(-turn_speed, turn_speed)
        if self.pixy.value(1) > 170:
            self.drive(turn_speed, -turn_speed)
        if self.pixy.value(1) > 150 and self.pixy.value(1) < 170:
            self.stop_both()

        time.sleep(0.25)

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()