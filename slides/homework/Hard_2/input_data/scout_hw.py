"""Scout 2 over CAN with the ugv_sdk Python binding (no ROS).

    ./src/ugv_sdk/scripts/bringup_can2usb_500k.bash     # once per boot / replug
    python scout_hw.py                                   # prints the reported motion for 3 s

Keep the area clear and the remote controller in your hand.
"""
import time

from ugv_sdk_py import ProtocolVersion
from ugv_sdk_py.scout_robot import ScoutRobot


class Scout:
    name = "Scout 2"

    def __init__(self, can="can0"):
        self.robot = ScoutRobot(ProtocolVersion.AGX_V2, False)
        self.robot.connect(can)
        self.robot.enable_commanded_mode()

    def velocity(self):
        """(linear m/s, angular rad/s) as reported by the robot."""
        m = self.robot.get_robot_state().motion_state
        return m.linear_velocity, m.angular_velocity

    def set_velocity(self, linear, angular):
        self.robot.set_motion_command(linear, angular)

    def stop(self):
        self.set_velocity(0.0, 0.0)


if __name__ == "__main__":
    bot = Scout()
    try:
        for _ in range(30):
            print(bot.name, bot.velocity())
            time.sleep(0.1)
    finally:
        bot.stop()
