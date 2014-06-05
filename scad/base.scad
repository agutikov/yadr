
include <servo_mount_module.scad>;

// расстояние от середины крепления сервы до плоскости в которой движется рука
arm_servo_offset=20;
// смещение оси относительно середины сервы
// предполагается что серва в servo_mount ложится симметрично
servo_arm_axis_offset=15;
// расстояние от центра до оси сервы
arm_axis_r=125;

arm_thickness=5;


module srv()
{
	translate([arm_axis_r-servo_arm_axis_offset,
				arm_servo_offset, 0])
	{
		servo_mount();
	}
	translate([100, 0, 5])
	cube(size=[200, arm_thickness, 10], center=true);
}

// translating - for printing into ps file
projection()
translate([arm_axis_r*0.75, arm_axis_r*1.1, 0])
{
	srv();
	rotate(a=120, v=[0,0,1]) srv();
	rotate(a=240, v=[0,0,1]) srv();
}
