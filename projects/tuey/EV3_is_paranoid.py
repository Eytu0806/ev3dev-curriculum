
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

    speech = 0

    while not robot.touch_sensor.is_pressed:
        width_value = robot.pixy.value(3)
        if robot.man_up_value == 1:
            print("Man level is 1")
            robot.pixy.mode = "SIG1"
        elif robot.man_up_value == 2:
            print("Man level is 2")
            robot.pixy.mode = "SIG2"
        elif robot.man_up_value == 3:
            print("Man level is 3")
            robot.pixy.mode = "SIG3"
        elif robot.man_up_value == 4:
            print("Man level is 4")
            robot.pixy.mode = "SIG4"
        elif robot.man_up_value == 5:
            print("Man level is 5")
            robot.pixy.mode = "SIG5"
        elif robot.man_up_value == 6:
            print("Man level is 6")
            robot.pixy.mode = "SIG6"
        elif robot.man_up_value == 7:
            ev3.Sound.play("/home/robot/csse120/assets/sounds/female_scream.wav")
            print("Man level is 7")
            robot.pixy.mode = "SIG7"

        # When man_up_value is 0, then the robot ignores this.
        if width_value > 0 and speech == 0:
            run_away(robot)
            ev3.Sound.speak("Lets never go there again").wait()
            computer_advice('Dialogue Number:',speech, "of 4")
            speech = speech + 1
        elif width_value > 0 and speech == 1:
            run_away(robot)
            ev3.Sound.speak("Why do you have to do this").wait()
            computer_advice('Dialogue Number:', speech, "of 4")
            speech = speech + 1
        elif width_value > 0 and speech == 2:
            run_away(robot)
            ev3.Sound.speak("That was so scary").wait()
            computer_advice('Dialogue Number:', speech, "of 4")
            speech = speech + 1
        elif width_value > 0 and speech == 3:
            run_away(robot)
            ev3.Sound.speak("What was that").wait()
            computer_advice('Dialogue Number:', speech, "of 4")
            speech += 1
        elif width_value > 0 and speech == 4:
            run_away(robot)
            ev3.Sound.speak("What did I just see").wait()
            computer_advice('Dialogue Number:', speech, "of 4")
            speech = 0

def computer_advice(advice1,advice2,advice3):
    print("-----------------Computer:------------------")
    print(str(advice1,advice2,advice3))
    print("--------------------------------------------")
def run_away(robot):
    print("-----------------Computer:------------------")
    print("EV3 is scared!")
    print("--------------------------------------------")
    ev3.Sound.play("/home/robot/csse120/assets/sounds/female_scream.wav")
    robot.turn_degrees(180, 800)
    time.sleep(1)
    robot.drive(700, 700)
    time.sleep(3)
    robot.stop_both()


main()
