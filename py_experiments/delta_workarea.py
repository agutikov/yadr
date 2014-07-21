#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import sys
import io
from pprint import pprint
from sympy import *
from mpmath import degrees,radians
import pickle

init_printing(use_unicode=True, use_latex=False)



'''
	большой треугольник в горизонтальной плоскости свехру - база
	маленький треугольник в горизонтальной плоскости снизу - эффектор
	сервы устанавливаются на базу
	то что крепится к сервам - руки или плечи
	то что крепится к эффектору - дельты или тяги

	начало координат - в центре базы
	b - расстояние от базы до оси руки
	Lb - длинна руки
	f - расстояние от центра еффектора до точки крепления тяги
	Lf - длинна тяги
	углы поворота плеч - theta1, theta2, theta3 - положительные вверх, отрицательные вниз

	Переходим в цилиндрическую систему координат.
	Первое плечо расположено вдоль оси alfa=0
	Два других, соответственно, вдоль alfa=2*pi/3 и alfa=-2*pi/3 (alfa=4*pi/3)


'''

b, Lb, f, Lf = symbols('b Lb f Lf')
theta1, theta2, theta3 = symbols('theta1 theta2 theta3')

# координаты центров сфер
# Ri = b - f + Lb*cos(theta1)
R1,R2,R3 = symbols('R1 R2 R3')


# координаты плоскости в которой находится эффектор
z = symbols('z')


# радиусы окружностей - сечений сфер плоскостью
r1,r2,r3 = symbols('r1 r2 r3')


# радиус-вектор эффектора в плоскости z
r, phi = symbols('r phi')

# уравнения для радиус-вектора положения эффектора
# ri^2 = Ri^2 + r^2 - 2*Ri*r*cos(psi + pi - alfa_i)

eq1 = Eq(r**2 - 2*r*R1*cos(phi + pi - 0)      + R1**2 - r1**2, 0)
eq2 = Eq(r**2 - 2*r*R2*cos(phi + pi - 2*pi/3) + R2**2 - r2**2, 0)
eq3 = Eq(r**2 - 2*r*R3*cos(phi + pi - 4*pi/3) + R3**2 - r3**2, 0)

print("\n\nEquations with z, r, phi:")
print("\n\n(1)")
pprint(eq1)
print("\n\n(2)")
pprint(eq2)
print("\n\n(3)")
pprint(eq3)


print("\n\nSolve (1) for r:")
solutions_1 = solve(eq1, r)
pprint(solutions_1)

print("\n\nSolve (2) for r:")
solutions_2 = solve(eq2, r)
pprint(solutions_2)

print("\n\nSolve (3) for r:")
solutions_3 = solve(eq3, r)
pprint(solutions_3)




# координаты центров сфер
Ro1,Ro2,Ro3 = symbols('Ro1 Ro2 Ro3')

Ro1 = b - f + Lb*cos(theta1)
Ro2 = b - f + Lb*cos(theta2)
Ro3 = b - f + Lb*cos(theta3)

print("\n\nRo1 =")
pprint(Ro1)
print("\n\nRo2 =")
pprint(Ro2)
print("\n\nRo3 =")
pprint(Ro3)



# высота центров сфер над плоскостью
h1,h2,h3 = symbols('h1 h2 h3')

h1 = z - Lb*sin(theta1)
h2 = z - Lb*sin(theta2)
h3 = z - Lb*sin(theta3)

# радиусы окружностей - сечений сфер плоскостью
ro1,ro2,ro3 = symbols('ro1 ro2 ro3')


ro1 = sqrt(Lf**2 - h1**2)
ro2 = sqrt(Lf**2 - h2**2)
ro3 = sqrt(Lf**2 - h3**2)

print("\n\nro1 =")
pprint(ro1)
print("\n\nro2 =")
pprint(ro2)
print("\n\nro3 =")
pprint(ro3)


for s in solutions_1:
	pprint(s.subs(R1, Ro1).subs(r1, ro1))

for s in solutions_2:
	pprint(s.subs(R2, Ro2).subs(r2, ro2))

for s in solutions_3:
	pprint(s.subs(R3, Ro3).subs(r3, ro3))





