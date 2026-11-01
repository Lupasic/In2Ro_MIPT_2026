"""Starter for the arm simulator: fill in dh() and fk(), then run  python dh_fk.py"""
import numpy as np

# UR5, standard DH, base frame as in the UR documentation: position (m) of the flange (tool0, the last link, no gripper) for three joint vectors (rad).
UR5_CHECK = [
    ([0, 0, 0, 0, 0, 0], [-0.81725, -0.19145, -0.00549]),
    ([0, -np.pi / 2, 0, -np.pi / 2, 0, 0], [0.0, -0.19145, 1.00106]),
    ([0.3, -1.2, 1.1, -0.7, 0.9, 0.4], [-0.58038, -0.34734, 0.50474]),
]


def dh(a, alpha, d, theta):
    """4x4 transform of one standard-DH row."""
    raise NotImplementedError


def fk(table, q):
    """Chain the rows of table = [(a, alpha, d, theta_offset), ...] for joint vector q; return the 4x4 base-to-TCP pose."""
    raise NotImplementedError


def check(table):
    for q, expected in UR5_CHECK:
        got = fk(table, q)[:3, 3]
        print("ok " if np.allclose(got, expected, atol=1e-4) else "BAD", np.round(got, 5), expected)


if __name__ == "__main__":
    print("build the UR5 table from the slide and call check(table)")
