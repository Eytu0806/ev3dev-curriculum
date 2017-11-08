
import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time

def main():
    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG1"
    width = robot.pixy.value(3)

    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc("35.194.247.175")
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.
    for speech in range(1):
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
        elif speech == 1:
            ev3.Speak.sound("Why do you have to do this").wait()
            computer_advice("Let's take it easy")
        elif speech == 2:
            ev3.Speak.sound("Im warning you").wait()
            computer_advice("He's having a rough day, maybe we should stop")
        elif speech == 3:
            ev3.Speak.sound("This is the last straw").wait()
            computer_advice("Uh oh...")
        elif speech == 4:
            ev3.Speak.sound("Thats it. Goodbye").wait()
            computer_advice("Look what you made him do!")
            mqtt_client.send_message("shutdown")
def computer_advice(advice):
    print("-----------------Computer:------------------")
    print(str(advice))
    print("--------------------------------------------")

main()
