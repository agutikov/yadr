
include <lib.scad>;

thikness = 2;

servo_width = 42;
servo_height = 20;
servo_length = 27;
servo_hole_d = 4;
servo_hole_h1 = 5;
servo_hole_h2 = 15;
servo_hole_margin = 4;

mount_margin_w = 15;
mount_hole_d = 4;
mount_hole_margin = 8;



module serv_mount()
{
	translate([mount_margin_w-thikness, -servo_length/2+thikness, 0])
	rotate(a=0, v=[0,0,1])
	cube(size=[thikness, servo_length-thikness, servo_height]);

	translate([0, -servo_length/2, 0])
	difference() {
		cube(size=[mount_margin_w, thikness, servo_height]);
		translate([servo_hole_margin, thikness, servo_hole_h1])
		true_hole(d=servo_hole_d, L=thikness*4);

		translate([servo_hole_margin, thikness, servo_hole_h2])
		true_hole(d=servo_hole_d, L=thikness*4);
	}
}

module servo_mount()
{
	difference() {
		translate([-servo_width/2 - mount_margin_w, -servo_length/2, 0])
			cube(size=[servo_width + mount_margin_w*2, servo_length, thikness]);

		translate([-servo_width/2 - mount_hole_margin, 0, -1])
		cylinder(r=mount_hole_d/2, h=thikness*4);

		translate([servo_width/2 + mount_hole_margin, 0, -1])
		cylinder(r=mount_hole_d/2, h=thikness*4);

		cube(center=true, esize=[]);
	}

	translate([servo_width/2, 0, thikness]) serv_mount();
	translate([-servo_width/2, 0, thikness]) mirror([1,0,0]) serv_mount();
}







