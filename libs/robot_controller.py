"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    
    # DONE: Implement the Snatch3r class as needed when working the sandbox exercises
    # (and delete these comments)
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.MAX_SPEED = 900
        self.Leds = ev3.Leds
        self.Sounds = ev3.Sound
        self.left_speed = 600
        self.right_speed = 600
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        self.man_up_value = 1
        self.follower = 0
        self.color = 0
        self.calibrate = 0
        self.time_s = 0
        self.user = 1
        self.SIG = "SIG1"
        self.finder = 0

        assert self.pixy

    def drive_inches(self, inches, both_sp):

        assert self.left_motor.connected
        assert self.right_motor.connected

        time_s = 1  # Any value other than 0.
        while time_s != 0:
            self.left_motor.run_to_rel_pos(speed_sp=both_sp, position_sp=90 * inches, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            self.right_motor.run_to_rel_pos(speed_sp=both_sp,position_sp=90*inches,stop_action=ev3.Motor.STOP_ACTION_BRAKE)

            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
            self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

            ev3.Sound.beep().wait()
            time_s = 0

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):

        assert self.left_motor.connected
        assert self.right_motor.connected

        revolutions = (6.5 * math.pi * (degrees_to_turn / 360)) / 3.7
        position = revolutions * 360

        time_s = 1  # Any value other than 0.
        while time_s != 0:

            self.left_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=-position, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp,position_sp=position,stop_action=ev3.Motor.STOP_ACTION_BRAKE)

            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
            self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

            ev3.Sound.beep().wait()
            time_s = 0

    def drive_polygon(self, speed, sides, side_length):

        for k in range(sides):
            self.drive_inches(side_length, speed)
            self.turn_degrees(180 - (((sides - 2) * 180) / sides), speed)

    def arm_calibration(self):

        assert self.arm_motor.connected
        assert self.touch_sensor.connected

        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)

        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)


        self.arm_motor.stop(stop_action="brake")

        ev3.Sound.beep().wait()

        self.arm_motor.run_to_rel_pos(position_sp=-5112, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.MediumMotor.STATE_RUNNING)

        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

        self.arm_motor.stop(stop_action="brake")

    def arm_up(self):

        assert self.arm_motor.connected
        assert self.touch_sensor.connected

        self.arm_motor.run_to_rel_pos(position_sp=5112, speed_sp=self.MAX_SPEED)

        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)

        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

    def arm_down(self):

        assert self.arm_motor.connected
        assert self.touch_sensor.connected

        self.arm_motor.run_to_rel_pos(position_sp=-5112, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.MediumMotor.STATE_RUNNING)  # Blocks until the motor finishes running
        self.arm_motor.stop(stop_action= "brake")
        ev3.Sound.beep().wait()

    def leftmotor_stop(self):

        assert self.left_motor.connected

        self.left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        # self.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)

    def rightmotor_stop(self):

        assert self.right_motor.connected

        self.right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        # self.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)

    def left_forward(self):

        assert self.left_motor.connected

        self.left_motor.run_forever(speed_sp=600)
        self.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)

    def left_backward(self):

        assert self.left_motor.connected

        self.left_motor.run_forever(speed_sp=-600)
        self.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)

    def right_forward(self):

        assert self.right_motor.connected

        self.right_motor.run_forever(speed_sp=600)
        self.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)

    def right_backward(self):

        assert self.right_motor.connected

        self.right_motor.run_forever(speed_sp=-600)
        self.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)

    def shutdown(self):

        self.Sounds.speak("Goodbye").wait()
        print("Goodbye!")

    def loop_forever(self):

        while True:
            time.sleep(.01)
            # self.color_test()

    def loop_until_object_is_detected(self, width):
        while not width > 0:
            time.sleep(.01)

    def drive(self, left_speed, right_speed):

        assert self.left_motor.connected
        assert self.right_motor.connected

        if self.user == 1:
            self.left_speed = left_speed
            self.right_speed = right_speed

            self.left_motor.run_forever(speed_sp=self.left_speed)
            self.right_motor.run_forever(speed_sp=self.right_speed)

    def man_up(self, value):

        self.man_up_value = value


    def stop_both(self):

        assert self.left_motor.connected
        assert self.right_motor.connected

        self.leftmotor_stop()
        self.rightmotor_stop()

    def find_color(self, color_var):

        assert self.color_sensor

        self.drive(300, 300)

        while not self.color_sensor.color == color_var:
            print(self.color_sensor.color)
            time.sleep(.01)

        self.stop_both()

    def read_reflected_light_intensity(self):

        assert self.color_sensor

        print(self.color_sensor.reflected_light_intensity)

    def follow_a_line(self, white_value, black_value):

        assert self.color_sensor
        assert self.left_motor.connected
        assert self.right_motor.connected


        while True:
            if self.color_sensor.reflected_light_intensity == black_value:
                self.drive(300,300)
            if self.color_sensor.reflected_light_intensity == white_value:
                self.drive(300,-300)
                while not self.color_sensor.reflected_light_intensity == black_value:
                    time.sleep(.01)
                self.stop_both()
            if self.touch_sensor.is_pressed:
                break
        self.stop_both()

    def proximity_test(self):

        assert self.ir_sensor

        while True:
            if self.ir_sensor.proximity < 10:
                self.Sounds.beep().wait()
                time.sleep(1.5)
            print(self.ir_sensor.proximity)
            time.sleep(.1)
            if self.touch_sensor.is_pressed:
                break

    def seek_beacon(self):
        """
        Uses the IR Sensor in BeaconSeeker mode to find the beacon.  If the beacon is found this return True.
        If the beacon is not found and the attempt is cancelled by hitting the touch sensor, return False.

        Type hints:
          :type robot: robo.Snatch3r
          :rtype: bool
        """

        # DONE: 2. Create a BeaconSeeker object on channel 1.

        forward_speed = 300
        turn_speed = 100
        BeaconSeaker = ev3.BeaconSeeker(channel=1)

        while not self.touch_sensor.is_pressed:
            # The touch sensor can be used to abort the attempt (sometimes handy during testing)

            # DONE: 3. Use the beacon_seeker object to get the current heading and distance.
            current_heading = BeaconSeaker.heading  # use the beacon_seeker heading
            current_distance = BeaconSeaker.distance  # use the beacon_seeker distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                self.stop_both()
            else:
                if math.fabs(current_heading) < 2:
                    # Close enough of a heading to move forward
                    print("On the right heading. Distance: ", current_distance)
                    # You add more!
                    if current_distance == 0:
                        time.sleep(1)
                        self.stop_both()
                        return True
                    if current_distance > 0:
                        self.drive(forward_speed, forward_speed)
                if math.fabs(current_heading) > 2 and math.fabs(current_heading) < 10:
                    if current_heading < 0:
                        self.drive(-turn_speed, turn_speed)
                    if current_heading > 0:
                        self.drive(turn_speed, -turn_speed)
                if math.fabs(current_heading) > 10:
                    self.stop_both()
                    print('Heading too far off')

            time.sleep(0.2)

    def new_drive_inches(self, drive_speed, inches):

        assert self.left_motor.connected
        assert self.right_motor.connected

        self.time_s = 1  # Any value other than 0.
        while self.time_s != 0:
            self.left_motor.run_to_rel_pos(speed_sp=drive_speed, position_sp=90 * inches, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            self.right_motor.run_to_rel_pos(speed_sp=drive_speed,position_sp=90*inches,stop_action=ev3.Motor.STOP_ACTION_BRAKE)

            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
            self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

            self.time_s = 0

    def new_turn_degrees(self, turn_speed, degree_of_turn):

        assert self.left_motor.connected
        assert self.right_motor.connected

        revolutions = (6.5 * math.pi * (degree_of_turn / 360)) / 3.7
        position = revolutions * 360

        self.time_s = 1  # Any value other than 0.
        while self.time_s != 0:

            self.left_motor.run_to_rel_pos(speed_sp=turn_speed, position_sp=-position, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            self.right_motor.run_to_rel_pos(speed_sp=turn_speed,position_sp=position,stop_action=ev3.Motor.STOP_ACTION_BRAKE)

            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
            self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

            self.time_s = 0

    def follow_color(self, drive_speed, turn_speed):

        cool_color = self.color
        self.user = 0
        self.calibrate = 0
        self.follower = 1
        print('Following a color')
        ev3.Sound.speak("Color Following").wait()
        time.sleep(.5)
        self.color_drive(drive_speed, drive_speed)
        while True:

            if self.follower == 0:
                break
            if self.color_sensor.color != cool_color:
                break
            time.sleep(.4)
        self.follower = 0
        self.stop_both()
        self.finder = 1
        self.find_drive(-turn_speed, turn_speed)
        while not self.color_sensor.color == self.color:
            time.sleep(.01)
        self.finder = 0
        self.stop_both()
        ev3.Sound.speak("Ready to be calibrated").wait()
        self.calibrate = 1

    def stop_follow(self):

        self.follower = 0
        self.stop_both()
        self.user = 1
        ev3.Sound.speak("You can control me").wait()

    def set_color(self, color_var):

        self.color = color_var
        print(self.color)
        if self.color == 2:
            self.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
            self.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
        if self.color == 3:
            self.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
            self.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        if self.color == 4:
            self.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)
            self.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
        if self.color == 5:
            self.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
            self.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)

    def start_calibrate(self):
        print('calibrating')
        self.user = 1

    def stop_calibrate(self):

        print('stopping calibration')
        self.user = 0
        self.stop_both()
        ev3.Sound.speak("Ready to Line follow").wait()

    def find_follow_color(self):
        self.calibrate = 1
        while self.color_sensor.color != self.color:
            self.calibrate_drive(500, 200)
            time.sleep(.1)
        self.stop_both()
        self.calibrate = 0
    def color_test(self):

        print(self.color_sensor.color)
        time.sleep(1)

    def color_drive(self, left_speed, right_speed):

        assert self.left_motor.connected
        assert self.right_motor.connected

        if self.follower == 1:
            self.left_speed = left_speed
            self.right_speed = right_speed

            self.left_motor.run_forever(speed_sp=self.left_speed)
            self.right_motor.run_forever(speed_sp=self.right_speed)

    def find_drive(self, left_speed, right_speed):

        assert self.left_motor.connected
        assert self.right_motor.connected

        if self.finder == 1:
            self.left_speed = left_speed
            self.right_speed = right_speed

            self.left_motor.run_forever(speed_sp=self.left_speed)
            self.right_motor.run_forever(speed_sp=self.right_speed)

    def calibrate_drive(self, left_speed, right_speed):

        assert self.left_motor.connected
        assert self.right_motor.connected

        if self.calibrate == 1:
            self.left_speed = left_speed
            self.right_speed = right_speed

            self.left_motor.run_forever(speed_sp=self.left_speed)
            self.right_motor.run_forever(speed_sp=self.right_speed)

    def color_to_look_for_red(self):
        self.pixy.mode = "SIG1"
        turn_speed = 100

        while not self.touch_sensor.is_pressed:

            print("value1: X", self.pixy.value(1))
            print("value2: Y", self.pixy.value(2))

            if self.pixy.value(1) < 150:
                self.drive(-turn_speed, turn_speed)
            if self.pixy.value(1) > 170:
                self.drive(turn_speed, -turn_speed)
            if self.pixy.value(1) > 150 and self.pixy.value(1) < 170:
                self.stop_both()

            time.sleep(0.25)

        print("Goodbye!")
        ev3.Sound.speak("Goodbye").wait()

    def set_SIG(self, SIG):
        self.SIG = SIG

    def automatic_drive(self):
        self.pixy.mode = self.SIG
        ev3.Sound.speak("Looking for criminal").wait(1000)
        self.turn_to_color()
        self.new_drive_inches(350, 24)
        ev3.Sound.speak("This is them").wait()
        time.sleep(1)
        self.new_turn_degrees(350, 180)
        self.new_seek_beacon()
        ev3.Sound.speak("Thank you officer").wait()

    def turn_to_color(self):
        while True:
            if self.pixy.value(1) < 150:
                self.drive(-200, 200)
            if self.pixy.value(1) > 170:
                self.drive(200, -200)
            if self.pixy.value(1) > 150 and self.pixy.value(1) < 170:
                self.stop_both()
                break

    def new_seek_beacon(self):
        forward_speed = 300
        turn_speed = 100
        BeaconSeaker = ev3.BeaconSeeker(channel=1)

        while True:

            current_heading = BeaconSeaker.heading  # use the beacon_seeker heading
            current_distance = BeaconSeaker.distance  # use the beacon_seeker distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                self.stop_both()
            else:
                if math.fabs(current_heading) < 2:
                    # Close enough of a heading to move forward
                    print("On the right heading. Distance: ", current_distance)
                    # You add more!
                    if current_distance == 0:
                        time.sleep(1)
                        self.stop_both()
                        return True
                    if current_distance > 0:
                        self.drive(forward_speed, forward_speed)
                if math.fabs(current_heading) > 2 and math.fabs(current_heading) < 10:
                    if current_heading < 0:
                        self.drive(-turn_speed, turn_speed)
                    if current_heading > 0:
                        self.drive(turn_speed, -turn_speed)
                if math.fabs(current_heading) > 10:
                    self.stop_both()
                    print('Heading too far off')

            time.sleep(0.2)