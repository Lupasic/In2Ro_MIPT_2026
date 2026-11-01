"""Limo (Ackermann mode) base through the pylimo serial API (no ROS).

    pip install pylimo==0.3.5
    python limo_hw.py            # prints the reported motion for 3 s

Put the robot in Ackermann mode first. Keep the wheels off the ground for the first test.
"""
import time

from pylimo import limo as pylimo


class Limo:
    name = "Limo CoRoT"

    def __init__(self, port="/dev/ttyTHS1"):
        self.robot = pylimo.LIMO(name=port)
        self.robot.EnableCommand()

    def state(self):
        """(linear m/s, steering angle rad) as reported by the robot. The reported and the commanded steering
        angle are not guaranteed to be on the same scale: finding the factor is part of Task 2."""
        return self.robot.GetLinearVelocity(), self.robot.GetSteeringAngle()

    def drive(self, linear, steering):
        """Linear speed m/s and steering angle rad (limited by the library)."""
        self.robot.SetMotionCommand(linear_vel=linear, steering_angle=steering)

    def stop(self):
        self.drive(0.0, 0.0)


if __name__ == "__main__":
    bot = Limo()
    try:
        for _ in range(30):
            print(bot.name, bot.state())
            time.sleep(0.1)
    finally:
        bot.stop()
