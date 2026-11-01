"""CSV logger shared by the three robot starters. First line names the robot."""
import csv
import time


class CsvLog:
    def __init__(self, path, robot, columns):
        self.f = open(path, "w", newline="")
        self.f.write(f"# robot: {robot}\n")
        self.w = csv.writer(self.f)
        self.w.writerow(["t"] + list(columns))
        self.t0 = time.monotonic()

    def row(self, *values):
        self.w.writerow([f"{time.monotonic() - self.t0:.3f}", *values])

    def close(self):
        self.f.close()
