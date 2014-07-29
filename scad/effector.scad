
include <config.scad>;
include <delta_mount_module.scad>;

R = D_effector_hole/2;

// размеры используемые при построении гайки
L = L_effector;
l = L/2;
base = sqrt(L*L - l*l);

r = d_effector/2;

// гайка с отверстиями - из шестиугольника вычтены отверстия
difference() {
	union() {
		// 6-angle
		linear_extrude(height = H_effector) {
			polygon(points=[ [base, -l], [base, l], [0, L], [-base, l], [-base, -l], [0, -L] ]);
		}
	}
	{
		// Hole in center
		cylinder(h = H_effector*2, r = R);

		for (a=[0 : 30 : 330]) {
			rotate(a=a, v=[0,0,1])
			translate([effector_drill_r_base, 0, 0])
			cylinder(h = H_effector*10, r = r);
		}
	}
}


module m2(a=0)
{
	rotate(a=a, v=[0,0,1])
	translate([base, L/2-cyl_w, 0])
	tricube(l=cyl_w, h=cyl_w, w=cyl_w);

	rotate(a=a, v=[0,0,1])
	mirror([0,1,0])
	translate([base, L/2-cyl_w, 0])
	tricube(l=cyl_w, h=cyl_w, w=cyl_w);

	rotate(a=a+30, v=[0,0,1])
	translate([0, base+cyl_r, cyl_r])
	delta_mount();

}

// далее 3 пары креплений
m2(a=0);
m2(a=120);
m2(a=240);




