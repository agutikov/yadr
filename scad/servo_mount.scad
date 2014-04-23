
thikness = 2;

servo_width = 50;
servo_height = 20;
servo_length = 30;
servo_hole_d = 4;
servo_hole_h1 = 7;
servo_hole_h2 = 15;
serv_hole_margin = 5;

mount_margin_w = serv_hole_margin*2 + thikness;
mount_hole_d = 4;

difference() {
	translate([-servo_width/2 - mount_margin_w, -servo_length/2, 0])
		cube(size=[servo_width + mount_margin_w*2, servo_length, thikness]);

	translate([-servo_width/2 - serv_hole_margin, 0, 0])
	cylinder(r=mount_hole_d/2, h=thikness*4);

	translate([servo_width/2 + serv_hole_margin, 0, 0])
	cylinder(r=mount_hole_d/2, h=thikness*4);
}

module serv_mount()
{
	translate([mount_margin_w, 0, 0])
	rotate(a=-90, v=[0,1,0])
	linear_extrude(height=thikness) {
		polygon(points=[[0, servo_length/2], [0, -servo_length/2], 
						 [servo_height, -servo_length/2 + thikness]]);
	}

	translate([0, -servo_length/2, 0])
	difference() {
		cube(size=[mount_margin_w, thikness, servo_height]);
		translate([serv_hole_margin, thikness*2, servo_hole_h1])
		rotate(a=90, v=[1,0,0])
			cylinder(r=servo_hole_d/2, h=thikness*4);

		translate([serv_hole_margin, thikness*2, servo_hole_h2])
		rotate(a=90, v=[1,0,0])
			cylinder(r=servo_hole_d/2, h=thikness*4);
	}
}

translate([servo_width/2, 0, thikness]) serv_mount();
translate([-servo_width/2, 0, thikness]) mirror([1,0,0]) serv_mount();







