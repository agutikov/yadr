
$fn=36;



// ширина промежутка между наружными краями конусов
delta_width=45;

// диаметр отверстия
bolt_d = 3;
bolt_r = bolt_d/2;

// цилиндр крепления тяг
cyl_w = 5;
cyl_d = 10;
cyl_r = cyl_d/2;

// конус крепления тяг
con_w = 5;
con_r = bolt_r+1;
con_d = con_r*2;



// толщина всего элемента эффектора
H_effector = 6;

// диаметр круглого большого отверстия в центре
D_effector_hole = 40;

// длина стороны эффектора
L_effector = delta_width-2*con_w;

// диаметр отверстия для крепления, которых 12 штук вокруг большого отверстия
d_effector = 4;

// радиус размещения отверстий для крепления
effector_drill_r_base = (D_effector_hole/2 + sqrt(L_effector*L_effector*3/4))/2;


finger_D = 10;
finger_H = 6;

