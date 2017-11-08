import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com

import ev3dev.ev3 as ev3
import time

import robot_controller as robo
man_up_value = 1
def EV3_is_Paranoid():
    print("-----------------Computer:------------------")
    print('Starting up EV3 is Paranoid')
    print("--------------------------------------------")
    for speech in range(5):
        def RobotControl():

            robot = robo.Snatch3r()
            robot.pixy.mode = "SIG1"
            width = robot.pixy.value(3)
            if width > 0 and man_up == 1:
                root.destroy()
                robot.stop_both()

                ev3.Sound.speak("ahhhhhhhhhhhhhhhhhhhhhhhhhh")

                robot.drive(-700, 700)
                time.sleep(.2)
                robot.drive(700, 700)
                time.sleep(5)
                robot.stop_both()
                time.sleep(1)

                if speech == 0:
                    ev3.Speak.sound("Lets never go there again").wait()
                    computer_advice('Maybe we should stay away from that')
                    root.destroy()
                elif speech == 1:
                    ev3.Speak.sound("Why do you have to do this").wait()
                    computer_advice("Let's take it easy")
                    root.destroy()
                elif speech == 2:
                    ev3.Speak.sound("Im warning you").wait()
                    computer_advice("He's having a rough day, maybe we should stop")
                    root.destroy()
                elif speech == 3:
                    ev3.Speak.sound("This is the last straw").wait()
                    computer_advice("Uh oh...")
                    root.destroy()
                elif speech == 4:
                    ev3.Speak.sound("Thats it. Goodbye").wait()
                    computer_advice("Look what you made him do!")
                    mqtt_client.send_message("shutdown")
                    root.destroy()
            root.after(500, RobotControl)
            # if speech == 3 and man_up_value == 1:
            #     root.destroy()
            #     for k in range(10):
            #         time.sleep(.5)
            #         print('Hello')
            # root.after(500, RobotControl)

        mqtt_client = com.MqttClient()
        mqtt_client.connect_to_ev3()

        root = tkinter.Tk()
        root.title("Human Control Panel")

        main_frame = ttk.Frame(root, padding=30, relief='raised')
        main_frame.grid()

        left_speed_label = ttk.Label(main_frame, text="Left")
        left_speed_label.grid(row=0, column=0)
        left_speed_entry = ttk.Entry(main_frame, width=8)
        left_speed_entry.insert(0, "600")
        left_speed_entry.grid(row=1, column=0)

        right_speed_label = ttk.Label(main_frame, text="Right")
        right_speed_label.grid(row=0, column=2)
        right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
        right_speed_entry.insert(0, "600")
        right_speed_entry.grid(row=1, column=2)

        forward_button = ttk.Button(main_frame, text="Forward")
        forward_button.grid(row=2, column=1)
        forward_button['command'] = lambda: drive(mqtt_client, left_speed_entry, right_speed_entry)
        root.bind('<Up>', lambda event: drive(mqtt_client, left_speed_entry, right_speed_entry))

        left_button = ttk.Button(main_frame, text="Left")
        left_button.grid(row=3, column=0)
        left_button['command'] = lambda: turn(mqtt_client, left_speed_entry, right_speed_entry, "left")
        root.bind('<Left>', lambda event: turn(mqtt_client, left_speed_entry, right_speed_entry, "left"))

        stop_button = ttk.Button(main_frame, text="Stop")
        stop_button.grid(row=3, column=1)
        stop_button['command'] = lambda: stop(mqtt_client)
        root.bind('<space>', lambda event: stop(mqtt_client))

        right_button = ttk.Button(main_frame, text="Right")
        right_button.grid(row=3, column=2)
        right_button['command'] = lambda: turn(mqtt_client, left_speed_entry, right_speed_entry, "right")
        root.bind('<Right>', lambda event: turn(mqtt_client, left_speed_entry, right_speed_entry, "right"))

        back_button = ttk.Button(main_frame, text="Back")
        back_button.grid(row=4, column=1)
        back_button['command'] = lambda: backward(mqtt_client, left_speed_entry, right_speed_entry)
        root.bind('<Down>', lambda event: backward(mqtt_client, left_speed_entry, right_speed_entry))

        up_button = ttk.Button(main_frame, text="Up")
        up_button.grid(row=5, column=0)
        up_button['command'] = lambda: send_up(mqtt_client)
        root.bind('<u>', lambda event: send_up(mqtt_client))

        down_button = ttk.Button(main_frame, text="Down")
        down_button.grid(row=6, column=0)
        down_button['command'] = lambda: send_down(mqtt_client)
        root.bind('<j>', lambda event: send_down(mqtt_client))

        q_button = ttk.Button(main_frame, text="Quit")
        q_button.grid(row=5, column=2)
        q_button['command'] = (lambda: quit_program(mqtt_client, False))

        e_button = ttk.Button(main_frame, text="Exit")
        e_button.grid(row=6, column=2)
        e_button['command'] = (lambda: quit_program(mqtt_client, True))

        man_up_EV3 = ttk.Button(main_frame, text="Man_up_EV3!")
        man_up_EV3.grid(row=7, column=1)
        man_up_EV3['command'] = (lambda: man_up_value(0))

        root.after(500, RobotControl())
        root.mainloop()

        print(speech)
        #TODO: Make un MAN UP button. If MAN UP is clicked, then
        #it makes man_up True, which neglects the if statement that makes it scared.
def man_up(value):
    man_up_value = value
    root = tkinter.Tk()
    root.title("Man up Successful!")
    main_frame = ttk.Frame(root, padding=30, relief='raised')
    main_frame.grid()
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
def computer_advice(advice):
    print("-----------------Computer:------------------")
    print(str(advice))
    print("--------------------------------------------")
EV3_is_Paranoid()

