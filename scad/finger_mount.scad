
include <config.scad>;

module mount() {
	difference() {
		union() {
			translate([effector_drill_r_base/2, 0, 0])
			cube(center=true, size=[effector_drill_r_base, finger_D, finger_H]);

			translate([effector_drill_r_base, 0, 0])
			cylinder(center=true, r=finger_D/2, h=finger_H);
		}
		translate([effector_drill_r_base, 0, 0])
		cylinder(center=true, r=d_effector/2, h=finger_H*2);
	}
}


difference() {
	union() {
		mount();

		rotate(a=120, v=[0,0,1])
		mount();

		rotate(a=240, v=[0,0,1])
		mount();

		cylinder(center=true, r=finger_D*1.5, h=finger_H);
	}
	union() {
		cylinder(center=true, r=finger_D/2, h=finger_H*2);

		translate([-finger_D, 0, 0])
		cylinder(center=true, r=bolt_r, h=finger_H*2);

		translate([finger_D, 0, 0])
		cylinder(center=true, r=bolt_r, h=finger_H*2);
	}
}


