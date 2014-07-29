
include <config.scad>;

difference() {
	cylinder(center=true, r=finger_D*1.5, h=finger_H);
	union() {
		cylinder(center=true, r=finger_D/2, h=finger_H*2);

		translate([-finger_D, 0, 0])
		cylinder(center=true, r=bolt_r, h=finger_H*2);

		translate([finger_D, 0, 0])
		cylinder(center=true, r=bolt_r, h=finger_H*2);
	}
}


