

include <delta_mount_module.scad>;

arm_w=5;

H=cyl_d;

W=delta_width-2*(cyl_w+con_w);

L=20;
T=4;

hole_d=3;

S=10;



module s1() 
{

//	Can't export to STL:
//	Simple:         no
//  Object isn't a valid 2-manifold

/*
	translate([delta_width/2-cyl_w-con_w, 0,0]) 
	rotate(a=-90, v=[0,0,1]) 
	arc(a=90, h=H, r2=cyl_w, r1=0);

	translate([delta_width/2-con_w, 0,0])
	rotate(a=90, v=[0,0,1])
	tricube(l=cyl_r, w=cyl_w, h=cyl_r);

	translate([delta_width/2-cyl_w-con_w, 0,H])
	rotate(a=180, v=[0,1,0])
	rotate(a=90, v=[0,0,1])
	tricube(l=cyl_r, w=cyl_w, h=cyl_r);
*/

	translate([W/2,-cyl_r,0])
	cube(size=[cyl_w, cyl_w+cyl_r, H]);
} 

module s2() 
{
	translate([-arm_w/2, -L-cyl_w, 0])
	rotate(a=90, v=[0,0,1])
	cube(size=[L, T, H]);
}


difference() {
	union() {
		
		translate([0,cyl_r,cyl_r]) 
		delta_mount();

		s1();
		mirror([1,0,0]) s1();

		translate([-W/2, -cyl_w, 0])
		cube(size=[W, cyl_w, H]);

		s2();
		mirror([1,0,0]) s2();

	}
	union() {
	
		translate([0, cyl_r, cyl_r])
		rotate(a=90, v=[0,0,1])
		true_hole(d=hole_d, L=delta_width+10);

		translate([0, -cyl_w-L/4, cyl_r])
		rotate(a=90, v=[0,0,1])
		true_hole(d=hole_d, L=delta_width);

		translate([0, -cyl_w-L/4-S, cyl_r])
		rotate(a=90, v=[0,0,1])
		true_hole(d=hole_d, L=delta_width);
	}
}






