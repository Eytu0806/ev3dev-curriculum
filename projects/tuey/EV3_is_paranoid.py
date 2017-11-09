
import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time

def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    print("-----------------Computer:------------------")
    print('Starting up EV3 is Paranoid')
    print("--------------------------------------------")
    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG1"
    speech = 0

    while not robot.touch_sensor.is_pressed:
        width_value = robot.pixy.value(3)
        if robot.man_up_value == 0:
            ev3.Sound.speak("Hahahahaha")
            break
        # When man_up_value is 0, then the robot ignores this.
        if width_value > 0 and speech == 0 and robot.man_up_value == 1:
            run_away()
            ev3.Sound.speak("Lets never go there again").wait()
            computer_advice('Maybe we should stay away from that')
            speech = speech + 1
        elif width_value > 0 and speech == 1 and robot.man_up_value == 1:
            run_away()
            ev3.Sound.speak("Why do you have to do this").wait()
            computer_advice("Let's take it easy")
            speech = speech + 1
        elif width_value > 0 and speech == 2 and robot.man_up_value == 1:
            run_away()
            ev3.Sound.speak("Im warning you").wait()
            computer_advice("He's having a rough day, maybe we should stop")
            speech = speech + 1
        elif width_value > 0 and speech == 3 and robot.man_up_value == 1:
            run_away()
            ev3.Sound.speak("This is the last straw").wait()
            computer_advice("Uh oh...")
            speech += 1
        elif width_value > 0 and speech == 4 and robot.man_up_value == 1:
            run_away()
            ev3.Sound.speak("Thats it. Goodbye").wait()
            computer_advice("Look what you made him do!")
            mqtt_client.send_message("shutdown")
            speech += 1
def computer_advice(advice):
    print("-----------------Computer:------------------")
    print(str(advice))
    print("--------------------------------------------")
def run_away():
    robot = robo.Snatch3r()
    robot.stop_both()
    ev3.Sound.speak("Uh oh")
    robot.turn_degrees(180, 800)
    time.sleep(2)
    robot.drive(700, 700)
    time.sleep(3)
    robot.stop_both()


main()
