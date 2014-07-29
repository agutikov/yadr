
include <config.scad>;
include <lib.scad>;

module mount()
{
	w=cyl_w+con_w+2;
	difference() {
		rotate(a=90, v=[1,0,0]) union() {
				translate([0,0,-cyl_w/2]) cylinder(center=true, r=cyl_r, h=cyl_w);
				translate([0,0,con_w/2]) cylinder(center=true, r1=cyl_r, r2=con_r, h=con_w);
		}
		translate([0,-(con_w-cyl_w)/2-1,0]) true_hole(d=bolt_d, L=w);
	}
};


module delta_mount() {
	w=delta_width/2-con_w;
	translate([w, 0, 0]) rotate(a=90, v=[0,0,1]) mount();
	mirror([1,0,0]) translate([w, 0, 0]) rotate(a=90, v=[0,0,1]) mount();
}


