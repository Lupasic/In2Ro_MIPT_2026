"""myCobot 280 arm on the Limo CoRoT, driven from Python (the Limo arm has no pendant).

    pip install pymycobot
    python limo_arm.py            # prints the joint angles and the end pose once

Angles in degrees, coordinates in mm and degrees (x, y, z, rx, ry, rz), speed 1-100.
"""
from pymycobot.mycobot280 import MyCobot280

PORT = "/dev/ttyUSB0"
BAUD = 115200
# Joint limits in degrees, J1..J6.
LIMITS = [(-168, 168), (-135, 135), (-150, 150), (-145, 145), (-165, 165), (-180, 180)]


class Arm:
    name = "Limo CoRoT arm"

    def __init__(self, port=PORT):
        self.mc = MyCobot280(port, BAUD)
        self.mc.power_on()

    def angles(self):
        return self.mc.get_angles()

    def coords(self):
        """[x, y, z, rx, ry, rz] of the flange in the base frame."""
        return self.mc.get_coords()

    def go_angles(self, angles, speed=30, tol=2.0):
        assert all(lo <= a <= hi for a, (lo, hi) in zip(angles, LIMITS)), "outside joint limits"
        self.mc.sync_send_angles(angles, speed)
        got = self.angles()
        if not got or max(abs(g - a) for g, a in zip(got, angles)) > tol:
            raise RuntimeError(f"joint target not reached: wanted {angles}, got {got}")

    def go_coords(self, coords, speed=30, linear=True, wait=True, tol=3.0):
        """wait=True blocks and checks the pose was reached (mm); wait=False sends the next command at once."""
        mode = 1 if linear else 0
        if wait:
            self.mc.sync_send_coords(coords, speed, mode)
            got = self.coords()
            if not got or max(abs(g - c) for g, c in zip(got[:3], coords[:3])) > tol:
                raise RuntimeError(f"pose not reached: wanted {coords}, got {got}")
        else:
            self.mc.send_coords(coords, speed, mode)

    def grip(self, close):
        self.mc.set_gripper_state(1 if close else 0, 50)


if __name__ == "__main__":
    arm = Arm()
    print(arm.name, arm.angles(), arm.coords())
