

H = 10;

R = 30;

thikness = 10;

base = R + thikness;

l = base*sqrt(3)/3;
L = sqrt(l*l + base*base);


r = 2;
r_base = R + thikness/2;
r_l = r_base/2;
r_L = sqrt(r_base*r_base - r_l*r_l);

r_bolt = 1.5;

difference() {
	
	// 6-angle 
	linear_extrude(height = H) {
		polygon(points=[ [base, -l], [base, l], [0, L], [-base, l], [-base, -l], [0, -L] ]);
	
	}
	{
		// Hole in center
		cylinder(h = H, r = R);

		translate([r_base, 0, 0]) cylinder(h = H, r = r);
		translate([-r_base, 0, 0]) cylinder(h = H, r = r);

		translate([-r_L, r_l, 0]) cylinder(h = H, r = r);
		translate([-r_L, -r_l, 0]) cylinder(h = H, r = r);

		translate([-r_l, r_L, 0]) cylinder(h = H, r = r);
		translate([-r_l, -r_L, 0]) cylinder(h = H, r = r);

		translate([r_L, r_l, 0]) cylinder(h = H, r = r);
		translate([r_L, -r_l, 0]) cylinder(h = H, r = r);

		translate([r_l, r_L, 0]) cylinder(h = H, r = r);
		translate([r_l, -r_L, 0]) cylinder(h = H, r = r);

		translate([0, r_base, 0]) cylinder(h = H, r = r);
		translate([0, -r_base, 0]) cylinder(h = H, r = r);
	}
}



A=10;
L2=30;

module mount(left=true) {
	  difference() {
		union() {
			cube(size=[L2, A, H], center=true);
			translate([L2/2, 0, 0]) rotate(a=90, v=[1,0,0]) cylinder(r=H/2, h=A, center=true);

			if (left) {
				translate([L2/2, A, 0]) rotate(a=90, v=[1,0,0]) cylinder(r2=H/2, r1=r_bolt+1, h=A/2);
			} else {
				translate([L2/2, -A/2, 0]) rotate(a=90, v=[1,0,0]) cylinder(r1=H/2, r2=r_bolt+1, h=A/2);
			}			
		}
		translate([L2/2, 0, 0]) rotate(a=90, v=[1,0,0]) cylinder(r=r_bolt, h=A*3, center=true);
	}
};

inside = false;

translate([base-A/2, l+A/2, A/2]) mount(!inside);
translate([base-A/2, -l-A/2, A/2]) mount(inside);

rotate(a=120, v=[0,0,1]) translate([base-A/2, l+A/2, A/2]) mount(!inside);
rotate(a=120, v=[0,0,1]) translate([base-A/2, -l-A/2, A/2]) mount(inside);

rotate(a=240, v=[0,0,1]) translate([base-A/2, l+A/2, A/2]) mount(!inside);
rotate(a=240, v=[0,0,1]) translate([base-A/2, -l-A/2, A/2]) mount(inside);




