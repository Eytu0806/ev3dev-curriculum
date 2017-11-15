
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com

mqtt_client = com.MqttClient()
mqtt_client.connect_to_ev3()

blue = 2
green = 3
yellow = 4
red = 5

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

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)

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

    direction_label_3 = ttk.Label(main_frame, text="Use the Colored Buttons to tell the robot to follow that colored line")
    direction_label_3.grid(row=6, column=3)

    start_follow_label = ttk.Label(main_frame, text="Press to Start following")
    start_follow_label.grid(row=7, column=3)
    start_follow_button = ttk.Button(main_frame, text="Start")
    start_follow_button.grid(row=7, column=1)

    stop_follow_label = ttk.Label(main_frame, text="Press to Stop Following and Switch to User Control")
    stop_follow_label.grid(row=8, column=3)
    stop_follow_button = ttk.Button(main_frame, text="Stop")
    stop_follow_button.grid(row=8, column=1)

    start_calibration_label = ttk.Label(main_frame, text="Press to Start Calibrating when the robot asks")
    start_calibration_label.grid(row=9, column=3)
    start_calibration_button = ttk.Button(main_frame, text="Calibrate")
    start_calibration_button.grid(row=9, column=1)

    stop_calibration_label = ttk.Label(main_frame, text="Press to Stop Calibration when robot is lined up")
    stop_calibration_label.grid(row=10, column=3)
    stop_calibration_button = ttk.Button(main_frame, text="Lined Up")
    stop_calibration_button.grid(row=10, column=1)

    find_color_label = ttk.Label(main_frame, text="Press to find color with magic")
    find_color_label.grid(row=11, column=3)
    find_color_button = ttk.Button(main_frame, text="Find Color")
    find_color_button.grid(row=11, column=1)

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

    green_button['command'] = lambda: set_color(mqtt_client, green)
    red_button['command'] = lambda: set_color(mqtt_client, red)
    yellow_button['command'] = lambda: set_color(mqtt_client, yellow)
    blue_button['command'] = lambda: set_color(mqtt_client, blue)

    start_calibration_button['command'] = lambda: start_calibrate(mqtt_client)
    stop_calibration_button['command'] = lambda: stop_calibrate(mqtt_client)

    start_follow_button['command'] = lambda: start_follow(mqtt_client, drive_speed_spin, turn_speed_spin)
    stop_follow_button['command'] = lambda: stop_follow(mqtt_client)

    find_color_button['command'] = lambda: find_color(mqtt_client)

    root.mainloop()

def drive(mqtt_client, drive_speed_spin):


    left_speed = int(drive_speed_spin.get())
    right_speed = int(drive_speed_spin.get())

    mqtt_client.send_message("drive", [left_speed, right_speed])

def backward(mqtt_client, drive_speed_spin):


    left_speed = int(drive_speed_spin.get())
    right_speed = int(drive_speed_spin.get())

    left_speed = -left_speed
    right_speed = -right_speed

    mqtt_client.send_message("drive", [left_speed, right_speed])

def stop(mqtt_client):


    mqtt_client.send_message("stop_both")

def turn(mqtt_client, turn_speed_spin, direction):


    left_speed = int(turn_speed_spin.get())
    right_speed = int(turn_speed_spin.get())

    if direction == "left":
        left_speed = -left_speed
        mqtt_client.send_message("drive", [left_speed, right_speed])

    elif direction == "right":
        right_speed = -right_speed
        mqtt_client.send_message("drive", [left_speed, right_speed])

def start_follow(mqtt_client, drive_speed_spin, turn_speed_spin):

    drive_speed = int(drive_speed_spin.get())
    turn_speed = int(turn_speed_spin.get())

    mqtt_client.send_message("follow_color", [drive_speed, turn_speed])

def stop_follow(mqtt_client):

    mqtt_client.send_message("stop_follow")

def set_color(mqtt_client, color):

    mqtt_client.send_message("set_color", [color])

def start_calibrate(mqtt_client):

    mqtt_client.send_message("start_calibrate")

def stop_calibrate(mqtt_client):

    mqtt_client.send_message("stop_calibrate")

def find_color(mqtt_client):

    mqtt_client.send_message("find_follow_color")

main()
