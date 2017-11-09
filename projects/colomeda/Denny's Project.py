
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com

mqtt_client = com.MqttClient()
mqtt_client.connect_to_ev3()

blue = 2
green = 3
yellow = 4
red = 5


def color_calibrate(mqtt_client, color):
    pass


def stop_follow(mqtt_client, new_color):

    mqtt_client.send_message("stop_follow")
    mqtt_client.send_message("set_color", [new_color])



def main():


    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    turn_speed_label = ttk.Label(main_frame, text="Turn Speed (100-900)")
    turn_speed_label.grid(row=0, column=0)
    turn_speed_spin = tkinter.Spinbox(main_frame, from_=100, to=900, width=8)
    turn_speed_spin.grid(row=1, column=0)

    drive_speed_label = ttk.Label(main_frame, text="Drive Speed (100-900)")
    drive_speed_label.grid(row=0, column=2)
    drive_speed_spin = tkinter.Spinbox(main_frame, from_=100, to=900, width=8, justify=tkinter.RIGHT)
    drive_speed_spin.grid(row=1, column=2)

    direction_label_1 = ttk.Label(main_frame, text="Use the SpinBoxes to the left to set turn/drive speed")
    direction_label_1.grid(row=0, column=3)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    # forward_button['command'] = lambda: drive(mqtt_client, drive_speed_spin, drive_speed_spin)
    # root.bind('<Up>', lambda event: drive(mqtt_client, drive_speed_spin, drive_speed_spin))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    # left_button['command'] = lambda: turn(mqtt_client, left_speed_entry, right_speed_entry, "left")
    # root.bind('<Left>', lambda event: turn(mqtt_client, left_speed_entry, right_speed_entry, "left"))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    # stop_button['command'] = lambda: stop(mqtt_client)
    # root.bind('<space>', lambda event: stop(mqtt_client))


    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    # right_button['command'] = lambda: turn(mqtt_client, left_speed_entry, right_speed_entry, "right")
    # root.bind('<Right>', lambda event: turn(mqtt_client, left_speed_entry, right_speed_entry, "right"))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    # back_button['command'] = lambda: backward(mqtt_client, drive_speed_spin, drive_speed_spin)
    # root.bind('<Down>', lambda event: backward(mqtt_client, drive_speed_spin, drive_speed_spin))

    direction_label_2 = ttk.Label(main_frame, text="If asked to help, use buttons to the left/arrow keys to help the robot!!")
    direction_label_2.grid(row=2, column=3)

    red_button = tkinter.Button(main_frame, text="Red", bg="black", fg="red")
    red_button.grid(row=5, column=0)

    blue_button = tkinter.Button(main_frame, text="Blue", fg="blue")
    blue_button.grid(row=5, column=1)

    yellow_button = tkinter.Button(main_frame, text="Yellow", bg="black", fg="yellow")
    yellow_button.grid(row=5, column=2)

    green_button = tkinter.Button(main_frame, text="Green", fg="green")
    green_button.grid(row=6, column=1)
    green_button['command'] = lambda:

    direction_label_3 = ttk.Label(main_frame, text="Use the Colored Buttons to tell the robot to follow that colored line")
    direction_label_3.grid(row=6, column=3)

    forward_button['command'] = lambda: drive(mqtt_client, drive_speed_spin)
    root.bind('<Up>', lambda event: drive(mqtt_client, drive_speed_spin))
    left_button['command'] = lambda: turn(mqtt_client, turn_speed_spin, "left")
    root.bind('<Left>', lambda event: turn(mqtt_client, turn_speed_spin, "left"))
    stop_button['command'] = lambda: stop(mqtt_client)
    root.bind('<space>', lambda event: stop(mqtt_client))
    right_button['command'] = lambda: turn(mqtt_client, turn_speed_spin, "right")
    root.bind('<Right>', lambda event: turn(mqtt_client, turn_speed_spin, "right"))
    back_button['command'] = lambda: backward(mqtt_client, drive_speed_spin)
    root.bind('<Down>', lambda event: backward(mqtt_client, drive_speed_spin))

    # up_button = ttk.Button(main_frame, text="Up")
    # up_button.grid(row=5, column=0)
    # up_button['command'] = lambda: send_up(mqtt_client)
    # root.bind('<u>', lambda event: send_up(mqtt_client))
    #
    # down_button = ttk.Button(main_frame, text="Down")
    # down_button.grid(row=6, column=0)
    # down_button['command'] = lambda: send_down(mqtt_client)
    # root.bind('<j>', lambda event: send_down(mqtt_client))
    #
    # q_button = ttk.Button(main_frame, text="Quit")
    # q_button.grid(row=5, column=2)
    # q_button['command'] = (lambda: quit_program(mqtt_client, False))
    #
    # e_button = ttk.Button(main_frame, text="Exit")
    # e_button.grid(row=6, column=2)
    # e_button['command'] = (lambda: quit_program(mqtt_client, True))



    root.mainloop()

def drive(mqtt_client, drive_speed_spin):
    if number == 1:
        print("drive forward")

        left_speed = int(drive_speed_spin.get())
        right_speed = int(drive_speed_spin.get())

        mqtt_client.send_message("drive", [left_speed, right_speed])

def backward(mqtt_client, drive_speed_spin):
    if number == 1:
        print("drive backward")

        left_speed = int(drive_speed_spin.get())
        right_speed = int(drive_speed_spin.get())

        left_speed = -left_speed
        right_speed = -right_speed

        mqtt_client.send_message("drive", [left_speed, right_speed])

def stop(mqtt_client):
    if number == 1:
        print("stop")

        mqtt_client.send_message("stop_both")

def turn(mqtt_client, turn_speed_spin, direction):
    if number == 1:
        print("turn", direction)

        left_speed = int(turn_speed_spin.get())
        right_speed = int(turn_speed_spin.get())

        if direction == "left":
            left_speed = -left_speed
            mqtt_client.send_message("drive", [left_speed, right_speed])

        elif direction == "right":
            right_speed = -right_speed
            mqtt_client.send_message("drive", [left_speed, right_speed])

main()
