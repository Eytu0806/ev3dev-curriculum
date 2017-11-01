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

        self.left_motor.stop()
        self.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)

    def rightmotor_stop(self):

        assert self.right_motor.connected

        self.right_motor.stop()
        self.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)

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

    def drive(self, left_speed, right_speed):

        assert self.left_motor.connected
        assert self.right_motor.connected

        self.left_speed = left_speed
        self.right_speed = right_speed

        self.left_motor.run_forever(speed_sp=self.left_speed)
        self.right_motor.run_forever(speed_sp=self.right_speed)

    def stop_both(self):

        assert self.left_motor.connected
        assert self.right_motor.connected

        self.leftmotor_stop()
        self.rightmotor_stop()

