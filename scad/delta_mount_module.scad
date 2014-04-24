
// ширина промежутка между выступающими креплениями
width=45;

// диаметр отверстия для крепления ball-joint-ов
d_bolt = 3;
r_bolt = d_bolt/2;

// ширина выступающих креплений
A = 5;
// ширина конуса
A_C = 5;
// толщина крепления,
H_z = 6;
// диаметр конуса
D_C = 10;
R_C = D_C/2;
// длина выступающих крепления, учитывать что они частично утоплены в гайку
L2 = 10;

inside = false;





// выступающее крепление ball-joint-а
// left - с какой стороны находится сужающийся цилиндр
// до смещения располагается в центре (учитывать при рассчёте смещения)
module mount(left=true) {
	translate([0, -L2/2, 0]) rotate(a=90, v=[0,0,1]) {

	  difference() {
		union() {
			cube(size=[L2, A, H_z], center=true);

			translate([0,0,R_C-H_z/2]) {
				translate([L2/2, 0, 0]) rotate(a=90, v=[1,0,0])
				cylinder(r=R_C, h=A, center=true);

				if (left) {
					translate([L2/2, A/2+A_C, 0]) rotate(a=90, v=[1,0,0])
					cylinder(r2=R_C, r1=r_bolt+1, h=A_C);
				} else {
					translate([L2/2, -A/2-A_C, 0]) rotate(a=90, v=[1,0,0])
					cylinder(r1=R_C, r2=r_bolt+1, h=A_C);
				}
			}
		}
		translate([L2/2, 0, R_C-H_z/2]) rotate(a=90, v=[1,0,0])
		cylinder(r=r_bolt, h=A*3, center=true);
	}

	}
};



module delta_mount() {
	w = -width/2 + A/2 + A_C;
	translate([w, 0, 0]) mount(!inside);
	mirror([1,0,0]) translate([w, 0, 0]) mount(!inside);
}




