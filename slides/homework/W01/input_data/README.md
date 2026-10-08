# AR-601M arm -- environment skeleton

This is a worked example of the packaging contract this homework asks
for, not a mandate to use Python.

- Either `pixi.toml` or `Dockerfile` sits at the repository root you
  submit, and one command reproduces every number your report quotes:
  `pixi run check`, or `docker build -t ar601m . && docker run ar601m`.
- The three required signatures are `FK(q, robot)`, `IK(T, robot)` and
  `DifferentialKinematics(q, robot)` -- see `src/kinematics.py` for what each must
  accept and return, and `tests/test_contract.py` for the checks that
  gate them (the contract only; never the answer).
- Also provide a runnable Task 2 angle-to-arm-and-pose visualizer, a Task 3
  all-valid-branches view with angle/residual labels, and both Task 6 maps.
  Your one command must reproduce the report's saved examples and figures.
- The language shown here -- Python, a hand-written `ar601m.yaml` reader,
  `pytest` -- is one example, not a requirement. Submit your own
  language's equivalent skeleton as long as it satisfies the same
  contract: one command, from a clean checkout, reproduces the report.
