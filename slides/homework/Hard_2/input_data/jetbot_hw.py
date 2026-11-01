"""JetBot motor board: wheel encoder ticks in, wheel speed commands out.

    pip install pyserial
    export ROBOT_ID=<number of your JetBot, 1-5>
    python jetbot_hw.py            # prints ticks for 3 s

Nothing here knows the wheel radius or the track width: finding them is the task.
"""
import os
import re
import sys
import threading
import time

import serial

DEVICE = "/dev/ttyMOTOR"
BAUD = 115200
COUNTS_PER_REV = 1760        # encoder counts per wheel revolution
MAX_RPM = 300                # wheel speed at command 1.0 (board scale is +-1000)
STALE_S = 0.5                # longest tolerated silence of the encoder stream
TICKS = re.compile(r"\$MAll:([-\d.]+),([-\d.]+)")


class JetBot:
    def __init__(self, device=DEVICE):
        self.robot_id = os.environ.get("ROBOT_ID", "")
        if self.robot_id not in ("1", "2", "3", "4", "5"):
            raise SystemExit("set ROBOT_ID to the number of your JetBot (1-5)")
        self.port = serial.Serial(device, BAUD, timeout=0.1)
        self.name = f"JetBot {self.robot_id}"
        self._ticks = None                 # nothing valid received yet
        self._stamp = None
        self._driving = False
        self._error = None
        self._alive = True
        self.port.reset_input_buffer()
        self.port.write(b"$upload:1,0,1#")       # stream ticks and speeds
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        try:
            while self._alive:
                m = TICKS.search(self.port.readline().decode(errors="ignore"))
                if self._driving and self._stamp is not None and time.monotonic() - self._stamp > STALE_S:
                    self._driving = False
                    self.port.write(b"$spd:0,0,0,0#\r")      # watchdog: the stream went silent
                if m:
                    # the board counts the right wheel backwards: flip it so both grow going forward
                    self._ticks = (float(m.group(1)), -float(m.group(2)))
                    self._stamp = time.monotonic()
        except Exception as exc:          # serial unplugged, board reset ...
            self._error = exc

    def ticks(self):
        """(left, right) encoder counts; both grow when the robot drives forward.
        Raises if the board has stopped reporting, so a stale value is never integrated."""
        if not self._fresh():
            self.stop()
            raise RuntimeError(f"no encoder data from the motor board: {self._error or 'timeout'}")
        return self._ticks

    def _fresh(self):
        if self._stamp is None:                      # wait for the first report
            end = time.monotonic() + 1.0
            while self._stamp is None and self._error is None and time.monotonic() < end:
                time.sleep(0.01)
        return self._error is None and self._stamp is not None and time.monotonic() - self._stamp <= STALE_S

    def set_wheel_speed(self, left, right):
        """Wheel speed commands in -1..1 (1 = MAX_RPM). Zero stops the robot.
        Refused while the encoder stream is stale."""
        if (left or right) and not self._fresh():
            self.stop()
            raise RuntimeError("encoder stream lost: refusing to drive")
        self._driving = bool(left or right)
        l, r = (int(max(-1.0, min(1.0, v)) * 1000) for v in (left, right))
        self.port.write(f"$spd:{l},{-r},0,0#\r".encode())

    def stop(self):
        self._driving = False
        self.port.write(b"$spd:0,0,0,0#\r")

    def close(self):
        self.stop()
        self._alive = False
        self.port.write(b"$upload:0,0,0#")
        self.port.close()


if __name__ == "__main__":
    bot = JetBot()
    try:
        for _ in range(30):
            print(bot.name, bot.ticks())
            time.sleep(0.1)
    finally:
        bot.close()
