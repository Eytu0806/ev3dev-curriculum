
import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com





def main():
    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    turn_speed_label = ttk.Label(main_frame, text="Turn Speed (0-900)")
    turn_speed_label.grid(row=0, column=0)
    turn_speed_spin = tkinter.Spinbox(main_frame, from_=0, to=900, width=8)
    turn_speed_spin.insert(0, "60")
    turn_speed_spin.grid(row=1, column=0)

    drive_speed_label = ttk.Label(main_frame, text="Drive Speed (0-900)")
    drive_speed_label.grid(row=0, column=2)
    drive_speed_spin = tkinter.Spinbox(main_frame, from_=0, to=900, width=8, justify=tkinter.RIGHT)
    drive_speed_spin.insert(0, "60")
    drive_speed_spin.grid(row=1, column=2)

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

    root.mainloop()

main()
