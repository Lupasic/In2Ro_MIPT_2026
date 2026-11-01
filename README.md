# Introduction to Robotics — MIPT, 2026

Introduction to Robotics (In2Ro) is a course on the mathematical and engineering foundations of robotic systems. Students study robot mechanisms, coordinate frames, forward and inverse kinematics, differential kinematics, workspaces and singularities, then apply these foundations to mobile robots, sensing, calibration and navigation. The repository contains lecture slides and homework materials for the course at MIPT.

## Course blocks

The course covers four broad areas:

- **Manipulation:** robot structure, transformations, forward and inverse kinematics, Jacobians, workspaces, singularities and motion.
- **Mobile robots:** locomotion, mobile-robot kinematics and motion control.
- **Sensors and Calibrations:** sensing, measurement quality, coordinate and temporal calibration, and state estimation.
- **Navigation:** localization, mapping, SLAM and path planning.

## Course materials and sources

The course draws on the following materials:

1. [Course Material Robotics 1 — Prof. Alessandro De Luca, Sapienza University of Rome](https://www.diag.uniroma1.it/deluca/rob1_en.php).
2. [Introduction to Robotics — Prof. Oussama Khatib, Stanford University](https://see.stanford.edu/Course/CS223A).
3. [Modern Robotics — Kevin M. Lynch and Frank C. Park, Northwestern University](https://www.youtube.com/playlist?list=PLggLP4f-rq02vX0OQQ5vrCxbJrzamYDfx).
4. [Advanced Robotics Manipulation — Prof. Alexander Klimchik, Innopolis University](https://eduwiki.innopolis.university/index.php/MSc%3A_Advanced_Robotics).
5. [Introduction to Autonomous Mobile Robots — Roland Siegwart, Illah Reza Nourbakhsh and Davide Scaramuzza](https://mitpress.mit.edu/9780262015356/introduction-to-autonomous-mobile-robots/).
6. [Probabilistic Robotics — Sebastian Thrun, Wolfram Burgard and Dieter Fox (Russian-language resource)](https://github.com/literator1996/veroyatnostnaya_robototehnica).

Slides may use publicly available material from these and other sources. Each lecture ends with references to the specific materials used in that lecture.

## Lecture slides

<!-- BEGIN GENERATED LECTURES -->
| Week | Topic | Materials |
|---:|---|---|
| 1 | Introduction | [PDF](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/lecture/W01/In2Ro_lec01.pdf) · [source](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/lecture/W01/In2Ro_lec01.tex) |
| 2 | Direct kinematics and DH notation | [PDF](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/lecture/W02/In2Ro_lec02.pdf) · [source](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/lecture/W02/In2Ro_lec02.tex) |
| 3 | Differential Kinematics | [PDF](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/lecture/W03/In2Ro_lec03.pdf) · [source](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/lecture/W03/In2Ro_lec03.tex) |
| 4 | Differential Kinematics | [PDF](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/lecture/W04/In2Ro_lec04.pdf) · [source](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/lecture/W04/In2Ro_lec04.tex) |
| 5 | Workspace and Singularities | [PDF](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/lecture/W05/In2Ro_lec05.pdf) · [source](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/lecture/W05/In2Ro_lec05.tex) |
| 6 | Programming real manipulators | [PDF](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/lecture/W06/In2Ro_lec06.pdf) · [source](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/lecture/W06/In2Ro_lec06.tex) |
| 7 | Mobile robots | [PDF](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/lecture/W07/In2Ro_lec07.pdf) · [source](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/lecture/W07/In2Ro_lec07.tex) |
| 8 | Wheel constraints and holonomy | [PDF](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/lecture/W08/In2Ro_lec08.pdf) · [source](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/lecture/W08/In2Ro_lec08.tex) |
<!-- END GENERATED LECTURES -->

## Homework

The homework deck and handout are available below. Quiz materials and homework solutions are kept in the private teaching repository.

<!-- BEGIN GENERATED HOMEWORK -->
| # | Topic | Materials |
|---:|---|---|
| 1 | The AR-601M arm | [PDF](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/homework/W01/In2Ro_hw01.pdf) · [source](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/homework/W01/In2Ro_hw01.tex) |
| Hard 1 | Manipulation: UR5, IIMT CI-05, Limo CoRoT arm | [PDF](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/homework/Hard_1/In2Ro_hw_hard1.pdf) · [source](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/homework/Hard_1/In2Ro_hw_hard1.tex) |
| Hard 2 | Mobile robots: JetBot, Scout 2, Limo CoRoT | [PDF](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/homework/Hard_2/In2Ro_hw_hard2.pdf) · [source](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/homework/Hard_2/In2Ro_hw_hard2.tex) |

[Homework 1 handout](https://github.com/Lupasic/In2Ro_MIPT_2026/blob/main/slides/homework/W01/resources/hw01_handout.pdf)
[Homework 1 starter files](https://github.com/Lupasic/In2Ro_MIPT_2026/tree/main/slides/homework/W01/input_data)
<!-- END GENERATED HOMEWORK -->

## Building the slides

Lecture and homework decks are built from the XeLaTeX source in this repository. The [latest successful build](https://github.com/Lupasic/In2Ro_MIPT_2026/actions/workflows/build.yml) also provides a downloadable artifact.

## Contributors

- Oleg Bulichev — course design, lectures and materials.
