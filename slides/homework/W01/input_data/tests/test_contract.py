"""Contract test for the ``input_data/`` skeleton.

Checks only the contract this skeleton promises, never an answer:

  - the model file loads and has six joints and four links, each with
    the fields a reader of the factor chain needs;
  - ``FK``, ``IK`` and ``Jacobian`` exist, are callable, and take the
    right number of arguments.

It does **not** check that ``FK`` returns a correct 4x4, that ``IK``
finds all valid branches, or that ``Jacobian`` matches a finite-difference
check -- those are the student's own tests to write once Tasks 2, 3, 4
and 5 replace the ``NotImplementedError`` stubs. A test suite that
passed those checks against this skeleton would prove nothing.

Run with: ``python -m pytest tests/ -q`` (or ``pixi run check``, or the
Dockerfile's default command).
"""
import inspect
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import robot_model  # noqa: E402
import kinematics  # noqa: E402


def test_model_file_loads_and_names_the_arm():
    robot = robot_model.load()
    assert robot["arm"] in ("right", "left")
    assert isinstance(robot["shoulder_offset_deg"], float)


def test_model_has_four_links_in_chain_order():
    robot = robot_model.load()
    names = [link["name"] for link in robot["links"]]
    assert names == ["l1", "l2", "l3", "l4"]


def test_model_has_six_joints_in_chain_order():
    robot = robot_model.load()
    names = [joint["name"] for joint in robot["joints"]]
    assert names == ["t1", "t2", "t3", "t4", "t5", "t6"]


def test_every_joint_is_revolute_with_a_two_sided_limit():
    robot = robot_model.load()
    for joint in robot["joints"]:
        assert joint["type"] == "R"
        lo, hi = joint["limit_deg"]
        assert lo < hi


def test_FK_exists_and_takes_two_arguments():
    assert callable(kinematics.FK)
    assert len(inspect.signature(kinematics.FK).parameters) == 2


def test_IK_exists_and_takes_two_arguments():
    assert callable(kinematics.IK)
    assert len(inspect.signature(kinematics.IK).parameters) == 2


def test_Jacobian_exists_and_takes_two_arguments():
    assert callable(kinematics.Jacobian)
    assert len(inspect.signature(kinematics.Jacobian).parameters) == 2


def test_the_stubs_still_raise_delete_this_test_once_you_implement_FK():
    """Documents intent, not a contract check. The moment Task 2 gives
    FK a real body this test starts failing -- correctly -- so delete it
    then rather than "fixing" it. Kept only so a freshly cloned skeleton
    does not silently look tested when nothing has been implemented yet.
    """
    with pytest.raises(NotImplementedError):
        kinematics.FK([0.0] * 6, robot_model.load())
