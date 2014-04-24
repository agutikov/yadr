
/*
	все размеры для удобства можно считать в миллиметрах
*/

include <delta_mount_module.scad>;

// толщина всего элемента
H = 6;

// диаметр круглого большого отверстия в центре
D = 40;
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



// гайка с отверстиями - из шестиугольника вычтены отверстия
difference() {
	union() {
		// 6-angle
		linear_extrude(height = H) {
			polygon(points=[ [base, -l], [base, l], [0, L], [-base, l], [-base, -l], [0, -L] ]);

		}

		// далее 3 пары выступающих креплений


		rotate(a=30, v=[0,0,1]) translate([0, R+thikness*1.5, H/2]) delta_mount();

		rotate(a=150, v=[0,0,1]) translate([0, R+thikness*1.5, H/2]) delta_mount();

		rotate(a=270, v=[0,0,1]) translate([0, R+thikness*1.5, H/2]) delta_mount();

	}
	{
		// Hole in center
		cylinder(h = H, r = R);

		translate([r_base, 0, 0]) cylinder(h = H*10, r = r);
		translate([-r_base, 0, 0]) cylinder(h = H*10, r = r);

		translate([-r_L, r_l, 0]) cylinder(h = H*10, r = r);
		translate([-r_L, -r_l, 0]) cylinder(h = H*10, r = r);

		translate([-r_l, r_L, 0]) cylinder(h = H*10, r = r);
		translate([-r_l, -r_L, 0]) cylinder(h = H*10, r = r);

		translate([r_L, r_l, 0]) cylinder(h = H*10, r = r);
		translate([r_L, -r_l, 0]) cylinder(h = H*10, r = r);

		translate([r_l, r_L, 0]) cylinder(h = H*10, r = r);
		translate([r_l, -r_L, 0]) cylinder(h = H*10, r = r);

		translate([0, r_base, 0]) cylinder(h = H*10, r = r);
		translate([0, -r_base, 0]) cylinder(h = H*10, r = r);
	}
}




