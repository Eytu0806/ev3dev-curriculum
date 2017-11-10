import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com

red = "SIG1"
green = "SIG2"
black = "SIG3"


# Selecting a color
def select_color_window():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Select Color")

    colors_frame = ttk.Frame(root, padding=20, relief='raised')
    colors_frame.grid()

    red_button = ttk.Button(colors_frame, text='Red')
    red_button.grid(row=1, column=1)
    red_button['command'] = lambda: set_color(mqtt_client, red, "red")

    green_button = ttk.Button(colors_frame, text='Green')
    green_button.grid(row=1, column=2)
    green_button['command'] = lambda: set_color(mqtt_client, green, "green")

    black_button = ttk.Button(colors_frame, text='Black')
    black_button.grid(row=1, column=3)
    black_button['command'] = lambda: set_color(mqtt_client, black, "black")

    root.mainloop()


def choose_mode():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Select Drive Style")

    drive_frame = ttk.Frame(root, padding=20, relief='raised')
    drive_frame.grid()

    manual_button = ttk.Button(drive_frame, text='Manual Drive')
    manual_button.grid(row=1, column=0)
    manual_button['command'] = lambda: manual_drive_controls()

    placeholder_label = ttk.Label(drive_frame, text='       ')
    placeholder_label.grid(row=1, column=1)

    automatic_button = ttk.Button(drive_frame, text='Automatic Drive')
    automatic_button.grid(row=1, column=2)
    automatic_button['command'] = lambda: automatic_drive(mqtt_client)

    root.mainloop()


# Manual Drive Controls:
def manual_drive_controls():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    # Creating Drive Window
    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = tkinter.Spinbox(main_frame, from_=0, to=900, width=8)
    left_speed_entry.insert(0, "60")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = tkinter.Spinbox(main_frame, from_=0, to=900, width=8)
    right_speed_entry.insert(0, "60")
    right_speed_entry.grid(row=1, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    # forward_button, 'Arrow Up' key, and 'w' key
    forward_button['command'] = lambda: drive(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Up>', lambda event: drive(mqtt_client, left_speed_entry, right_speed_entry))
    root.bind('w', lambda event: drive(mqtt_client, left_speed_entry, right_speed_entry))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    # left_button, '<Left>' key, and 'a' key
    left_button['command'] = lambda: turn(mqtt_client, left_speed_entry, right_speed_entry, "left")
    root.bind('<Left>', lambda event: turn(mqtt_client, left_speed_entry, right_speed_entry, "left"))
    root.bind('a', lambda event: turn(mqtt_client, left_speed_entry, right_speed_entry, "left"))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    # stop_button, '<space>' key, and 'Left Shift' key
    stop_button['command'] = lambda: stop(mqtt_client)
    root.bind('<space>', lambda event: stop(mqtt_client))
    root.bind('<Shift_L>', lambda event: stop(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    # right_button, '<Right>' key, and 'd' key
    right_button['command'] = lambda: turn(mqtt_client, left_speed_entry, right_speed_entry, "right")
    root.bind('<Right>', lambda event: turn(mqtt_client, left_speed_entry, right_speed_entry, "right"))
    root.bind('d', lambda event: turn(mqtt_client, left_speed_entry, right_speed_entry, "right"))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    # back_button, '<Down>' key, and 's' key
    back_button['command'] = lambda: backward(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Down>', lambda event: backward(mqtt_client, left_speed_entry, right_speed_entry))
    root.bind('s', lambda event: backward(mqtt_client, left_speed_entry, right_speed_entry))

    # Making the arm go up and down
    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Making the program quit when 'q' is pressed
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    # Making the program quit completely when 'e' is pressed
    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()


def drive(mqtt_client, left_speed_entry, right_speed_entry):
    print("drive forward")

    left_speed = int(left_speed_entry.get())
    right_speed = int(right_speed_entry.get())

    mqtt_client.send_message("drive", [left_speed, right_speed])


def backward(mqtt_client, left_speed_entry, right_speed_entry):
    print("drive backward")

    left_speed = int(left_speed_entry.get())
    right_speed = int(right_speed_entry.get())

    left_speed = -left_speed
    right_speed = -right_speed

    mqtt_client.send_message("drive", [left_speed, right_speed])


def stop(mqtt_client):
    print("stop")

    mqtt_client.send_message("stop_both")


def turn(mqtt_client, left_speed_entry, right_speed_entry, direction):
    print("turn", direction)

    left_speed = int(left_speed_entry.get())
    right_speed = int(right_speed_entry.get())

    if direction == "left":
        left_speed = -left_speed
        mqtt_client.send_message("drive", [left_speed, right_speed])

    elif direction == "right":
        right_speed = -right_speed
        mqtt_client.send_message("drive", [left_speed, right_speed])

    else:
        print("something is terribly wrong here")


def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def set_color(mqtt_client, color, led_color):
    print(color)
    send_led_command(mqtt_client, 'left', led_color)
    send_led_command(mqtt_client, 'right', led_color)
    mqtt_client.send_message("set_SIG", [color])
    choose_mode()


def send_led_command(mqtt_client, led_side, led_color):
    print("Sending LED side = {}  LED color = {}".format(led_side, led_color))
    mqtt_client.send_message("set_led", [led_side, led_color])


def set_automatic_color(mqtt_client, color):
    print("If you choose automatic, the robot will go to ", color)
    mqtt_client.send_message()

def automatic_drive(mqtt_client):
    mqtt_client.send_message("automatic_drive")

##############################################################################
# This is where the fun begins!
##############################################################################
select_color_window()          # Need a way to close the color window after selection without ending the entire program
