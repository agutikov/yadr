#!/usr/bin/python

import sys
import io
from pprint import pprint
from sympy import *
from mpmath import degrees,radians
import pickle

init_printing(use_unicode=True, use_latex=False)

'''

	Как эти все запчасти называются?

	r - половина расстояния между осями креплений первых плеч

	сверху короткое первое плечо
	s - его длина

	к нему крепится второе - длинное плечо
	l - его длинна

	a1 - угол между левым первым плечом и горизонталью
		пока будем считать что они опускается только вниз - тогда угол положительный и меньше 90
	b1 - то-же самое, но справа

	x,y - координаты места соединения вторых плеч
	x - слева-направо
	y - от крепления сервоприводов - к месту соединения вторых плеч

	xa,ya - координаты конца первого плеча слева
	xb,yb - то-же самое справа

	равенство длин вторых (длинных) плеч и прямоугольный треугольник с длинным плечом в качестве гипотенузы:
	l*l == (x - xa)*(x - xa) + (y - ya)*(y - ya) == (xb - x)*(xb - x) + (y - yb)*(y - yb)

'''

a1, b1, s, l, r, x, y = symbols('a1 b1 s l r x y')

xa = -r - s*cos(a1)
ya = s*sin(a1)
xb = r + s*cos(b1)
yb = s*sin(b1)

eq_a = Eq(l*l, (x - xa)*(x - xa) + (y - ya)*(y - ya))
eq_b = Eq(l*l, (xb - x)*(xb - x) + (y - yb)*(y - yb))

pprint(eq_a)
pprint(eq_b)

solutions = solve([eq_a, eq_b], [x, y])

for idx,s in enumerate(solutions):
	pickle.dump(s, open(str('sol_%02d.dat' % idx), 'wb'))

