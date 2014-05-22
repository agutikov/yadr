
Famous post about delta robot kinematics:
http://forums.trossenrobotics.com/tutorials/introduction-129/delta-robot-kinematics-3276/

TODO:

0. write and save as much info about hardware as possible
1. sample on python
2. basic simpliest firmware for stm32vl-discovery
3. full proto implementation
4. ? lisp on board

protocol:

1) EEPROM storage:
- geometry sizes of robot parts
- servo parameters:
    - pwm full period
    - pwm high level duration for both edges and zero (horisontal position)
    - parameters for algorithm for translating angle into pwm high level duration
- smoothing mode and prameters for them:
    - no smoothing
    - linear: constant speed
    - non-linear: accelerated motion - start, acceleration, highest speed, braking, stop
All parameters, stored at EEPROM can be readed and writed.

2) control commands:
- set for single servo or all servos:
    - set destination pwm high level duration
    - set destination angle
- set destination coordinates
- get smooth motion status (running or stopped)
- get smooth motion current parameters - speed for each pwm, angle, coordinates and effector velocity
- get current coordinates, angles, pwm high level durations

3) path calculation - ?
