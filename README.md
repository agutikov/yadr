Yet Another Delta Robot
=======================

http://hackerspace.by/projects/4


Content
-------

/scad/               - models for 3d printing 
/py_experiments/     - mostly with SymPy 
/firmware/           - firmware for Arduino UNO and STM32VL-Discovery 
delta_mouse.py       - demo application, delta's effector follows mouse, wheel is z-axis 



Make STLs for 3D printing
-------------------------

Need OpenSCAD.

```bash
cd /scad/
make
```

Make firmware for STM32VL-Discovery
-----------------------------------

Place STM32 standard periferal library into ../stm32/spl/STM32F10x_StdPeriph_Lib_V3.5.0/ 
Or edit the Makefile to change it's location - variable SPL_LIB_PATH 

For flashing need OpenOCD.

```bash
cd firmware/stm32/stm32vl_discovery/
make
make flash
```
