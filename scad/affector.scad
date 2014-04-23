
/* 
	все размеры для удобства можно считать в миллиметрах
*/

// толщина всего элемента
H = 10;

// диаметр круглого большого отверстия в центре
D = 60;
R = D/2;

// минимальная ширина стенок гайки
thikness = 10;

// размеры используемые при построении гайки
base = R + thikness;
l = base*sqrt(3)/3;
L = sqrt(l*l + base*base);

// диаметр отверстия для крепления, которых 12 штук по вокруг большого отверстия
d = 4;
r = d/2;

// размеры используемые для размещения отверстий для крепления
r_base = R + thikness/2;
r_l = r_base/2;
r_L = sqrt(r_base*r_base - r_l*r_l);

// диаметр отверстия для крепления ball-joint-ов
d_bolt = 3;
r_bolt = d_bolt/2;

// ширина выступающих креплений
A = 10;
// длина выступающих крепления, учитывать что они частично утоплены в гайку
L2 = 30;

// с какой стороны крепятся ball-joint-ы
// и соответсвенно находятся конусы
// false - с наружней
// true - с внутренней
inside = false;


// гайка с отверстиями - из шестиугольника вычтены отверстия
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

// выступающее крепление ball-joint-а
// left - с какой стороны находится сужающийся цилиндр
// до смещения располагается в центре (учитывать при рассчёте смещения)
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

// далее 3 пары выступающих креплений

translate([base-A/2, l+A/2, A/2]) mount(!inside);
translate([base-A/2, -l-A/2, A/2]) mount(inside);

rotate(a=120, v=[0,0,1]) translate([base-A/2, l+A/2, A/2]) mount(!inside);
rotate(a=120, v=[0,0,1]) translate([base-A/2, -l-A/2, A/2]) mount(inside);

rotate(a=240, v=[0,0,1]) translate([base-A/2, l+A/2, A/2]) mount(!inside);
rotate(a=240, v=[0,0,1]) translate([base-A/2, -l-A/2, A/2]) mount(inside);




