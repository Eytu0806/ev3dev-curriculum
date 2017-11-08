import tkinter
from tkinter import ttk
def main():
    for k in range(5):
        def periodically_called():
            print("test")
            root.after(10, periodically_called)
        root = tkinter.Tk()

        main_frame = ttk.Frame(root, padding=30, relief = "raised")
        main_frame.grid()

        suppress_button = ttk.Button(main_frame, text="suppress")
        suppress_button.grid()
        suppress_button['command'] = lambda: print('suppressed')

        root.after(10, periodically_called())
        root.mainloop()
main()
