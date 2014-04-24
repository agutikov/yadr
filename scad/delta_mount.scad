
include <delta_mount_module.scad>;


w = 6;

delta_mount();



translate([0, -L2+A/2, 0]) cube(center=true, size=[width-A_C*2, A, H_z]);


L1 = 30;

difference() {
	union() {
		translate([w/2, -L1-R_C, -H_z/2]) cube(size=[w/2, L1, H_z*1.5]);
		mirror([1,0,0]) translate([w/2, -L1-R_C, -H_z/2]) cube(size=[w/2, L1, H_z*1.5]);
	}
	union() {
		translate([-width/2, -15, H_z/2-1]) rotate(a=90, v=[0,1,0]) cylinder(r=2, h=width);
		translate([-width/2, -30, H_z/2-2]) rotate(a=90, v=[0,1,0]) cylinder(r=2, h=width);

	}
}
















;