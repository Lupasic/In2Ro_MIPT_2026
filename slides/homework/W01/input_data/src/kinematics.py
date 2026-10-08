"""Kinematics stubs for the AR-601M arm skeleton.

Fill these in as you complete Tasks 2, 3, 4 and 5 of the homework. Every
function's docstring states exactly what it must accept and return; the
contract test (``tests/test_contract.py``) checks the signature and the
model file, never the answer -- getting these three functions right is
your job, not something the skeleton can verify for you.
"""


def FK(q, robot):
    """Forward kinematics.

    q: six joint values, in radians -- every joint of this arm is
       revolute -- in the order t1..t6 that ``robot["joints"]`` lists
       them.
    robot: the dict returned by ``robot_model.load()``.

    Returns: a 4x4 homogeneous transform (a list of 4 lists of 4 floats,
    or your own matrix type) carrying the base frame to the tool frame.

    This is Task 2.
    """
    raise NotImplementedError("Task 2")


def IK(T, robot):
    """Inverse kinematics.

    T: a 4x4 homogeneous transform, base frame to tool frame -- the
       target pose.
    robot: the dict returned by ``robot_model.load()``.

    Returns: a list of unique joint-value tuples ``q`` (radians), one per
    isolated branch that reaches ``T`` within the declared joint limits.
    The analytical route of Task 3 enumerates every valid branch; the
    numerical route of Task 4 may find only one branch from a given seed.
    An analytically proven unreachable target returns an empty list.
    Handle a non-isolated singular family explicitly and document its
    representation rather than counting sampled members as finite.

    This is Task 3 (analytical) and Task 4 (numerical).
    """
    raise NotImplementedError("Task 3")


def DifferentialKinematics(q, robot):
    """Differential kinematics.

    q: six joint values, same convention as ``FK``.
    robot: the dict returned by ``robot_model.load()``.

    Returns: a 6x6 matrix (a list of 6 lists of 6 floats, or your own
    matrix type). Its top three rows map joint rates to the tool's linear
    velocity; its bottom three rows map them to its angular velocity.

    This is Task 5.
    """
    raise NotImplementedError("Task 5")
