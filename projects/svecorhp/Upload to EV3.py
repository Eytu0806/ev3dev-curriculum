import mqtt_remote_method_calls as com
import robot_controller as robo

import ev3dev.ev3 as ev3
import time


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    # robot.arm_calibration()

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()

    # Buttons on EV3 (these obviously assume TO DO: 3. is done)
    btn = ev3.Button()
    btn.on_up = lambda state: handle_button_press(state, mqtt_client, "Up")
    btn.on_down = lambda state: handle_button_press(state, mqtt_client, "Down")
    btn.on_left = lambda state: handle_button_press(state, mqtt_client, "Left")
    btn.on_right = lambda state: handle_button_press(state, mqtt_client, "Right")
    btn.on_backspace = lambda state: handle_shutdown(state, my_delegate)

    while my_delegate.running:
        btn.process()
        time.sleep(0.01)

    ev3.Sound.speak("Goodbye").wait()
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)

    robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.


class MyDelegate(object):

    def __init__(self):
        self.running = True

    def set_led(self, led_side_string, led_color_string):

        print("Received: {} {}".format(led_side_string, led_color_string))
        led_side = None

        if led_side_string == "left":
            led_side = ev3.Leds.LEFT
        elif led_side_string == "right":
            led_side = ev3.Leds.RIGHT

        led_color = None
        if led_color_string == "green":
            led_color = ev3.Leds.GREEN
        elif led_color_string == "red":
            led_color = ev3.Leds.RED
        elif led_color_string == "black":
            led_color = ev3.Leds.BLACK

        if led_side is None or led_color is None:
            print("Invalid parameters sent to set_led. led_side_string = {} led_color_string = {}".format(
                led_side_string, led_color_string))
        else:
            ev3.Leds.set_color(led_side, led_color)


# ----------------------------------------------------------------------
# Button event callback functions
# ----------------------------------------------------------------------
def handle_button_press(button_state, mqtt_client, button_name):
    """Handle IR / button event."""
    if button_state:
        print("{} button was pressed".format(button_name))

        mqtt_client.send_message("button_pressed", [button_name])


def handle_shutdown(button_state, my_delegate):
    """Exit the program."""
    if button_state:
        my_delegate.running = False


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()


