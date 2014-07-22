#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import sys
import io
from pprint import pprint
from sympy import *
from mpmath import degrees,radians
import pickle
import math

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
# ri^2 = Ri^2 + r^2 - 2*Ri*r*cos(alfa - phi)

eq1 = Eq(r**2 - 2*r*R1*cos(phi)      + R1**2 - r1**2, 0)
eq2 = Eq(r**2 - 2*r*R2*cos(2*pi/3 - phi) + R2**2 - r2**2, 0)
eq3 = Eq(r**2 - 2*r*R3*cos(4*pi/3 - phi) + R3**2 - r3**2, 0)

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




# замена косинусов и синусов
C1,C2,C3 = symbols('C1 C2 C3')
S1,S2,S3 = symbols('S1 S2 S3')

C1 = cos(theta1)
C2 = cos(theta2)
C3 = cos(theta3)

S1 = sin(theta1)
S2 = sin(theta2)
S3 = sin(theta3)


c1,c2,c3 = symbols('c1 c2 c3')
s1,s2,s3 = symbols('s1 s2 s3')

'''
s1 = sqrt(1 - c1**2)
s2 = sqrt(1 - c2**2)
s3 = sqrt(1 - c3**2)
'''

# координаты центров сфер
Ro1,Ro2,Ro3 = symbols('Ro1 Ro2 Ro3')

Ro1 = b - f + Lb*c1
Ro2 = b - f + Lb*c2
Ro3 = b - f + Lb*c3

print("\n\nRo1 =")
pprint(Ro1)
print("\n\nRo2 =")
pprint(Ro2)
print("\n\nRo3 =")
pprint(Ro3)



# высота центров сфер над плоскостью
h1,h2,h3 = symbols('h1 h2 h3')

h1 = z - Lb*s1
h2 = z - Lb*s2
h3 = z - Lb*s3

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
	print("\n\nSolution (1) for r:")
	pprint(s.subs(R1, Ro1).subs(r1, ro1).subs(c1, C1).subs(s1, S1))

for s in solutions_2:
	print("\n\nSolution (2) for r:")
	pprint(s.subs(R2, Ro2).subs(r2, ro2).subs(c2, C2).subs(s2, S2))

for s in solutions_3:
	print("\n\nSolution (3) for r:")
	pprint(s.subs(R3, Ro3).subs(r3, ro3).subs(c3, C3).subs(s3, S3))


Theta = [pi/4, -pi/4]

LB = 130
LF = 320
B = 120
F = 50

def subs_sol (Z, Phi):
	values = []

	for t in Theta:
		for s in solutions_1:
			r = s.subs(R1, Ro1).subs(r1, ro1).subs(c1, C1).subs(s1, S1).subs(theta1, t).subs(Lb, LB).subs(Lf, LF).subs(b, B).subs(f, F).subs(z, Z).subs(phi, Phi).evalf(4)
			values.append(r)

		for s in solutions_2:
			r = s.subs(R2, Ro2).subs(r2, ro2).subs(c2, C2).subs(s2, S2).subs(theta2, t).subs(Lb, LB).subs(Lf, LF).subs(b, B).subs(f, F).subs(z, Z).subs(phi, Phi).evalf(4)
			values.append(r)

		for s in solutions_3:
			r = s.subs(R3, Ro3).subs(r3, ro3).subs(c3, C3).subs(s3, S3).subs(theta3, t).subs(Lb, LB).subs(Lf, LF).subs(b, B).subs(f, F).subs(z, Z).subs(phi, Phi).evalf(4)
			values.append(r)

	pprint(values)
	print()

	return values



print("\n"*4)

r_data = []
phi_data = []

for Z in [-400, -300, -200, -100, -50, 0, 50, 100, 200, 300, 400]:
	_phi_data = []
	_r_data = []

	for p in range(0, 37):
		Phi = p*math.pi/18
		arr = list(filter(lambda x: x > 0, filter(lambda z: im(z) == 0, subs_sol(Z, Phi))))
		if len(arr) > 0:
			_r = min(arr)
			_phi_data.append(Phi)
			_r_data.append(_r)

	r_data.append(_r_data)
	phi_data.append(_phi_data)


import matplotlib.pyplot as plt



ax = plt.subplot(111, polar=True)

for idx,r_dat in enumerate(r_data):
	ax.plot(phi_data[idx], r_dat, linewidth=3)


ax.grid(True)

ax.set_title("A line plot on a polar axis", va='bottom')
plt.show()




quit()

################################################################################

print("\n\nEquations with z, r, phi:")
eq4 = eq1.subs(R1, Ro1).subs(r1, ro1)
print("\n\n(4)")
pprint(eq4)

eq5 = eq2.subs(R2, Ro2).subs(r2, ro2)
print("\n\n(5)")
pprint(eq5)

eq6 = eq3.subs(R3, Ro3).subs(r3, ro3)
print("\n\n(6)")
pprint(eq6)


print("\n\nSimplify equations with z, r, phi:")
eq7 = eq4.expand().simplify()
print("\n\n(7)")
pprint(eq7)

eq8 = eq5.expand().simplify()
print("\n\n(8)")
pprint(eq8)

eq9 = eq6.expand().simplify()
print("\n\n(9)")
pprint(eq9)


'''

print("\n\nSolve (7) for c1:")
solutions_7 = solve(eq7, c1)
pprint(solutions_7)

print("\n\nSolve (8) for c2:")
solutions_8 = solve(eq8, c2)
pprint(solutions_8)

print("\n\nSolve (9) for c3:")
solutions_9 = solve(eq9, c3)
pprint(solutions_9)

'''


print("\n\nEquation (21)")
eq21 = Eq(
	(
		c1 * (2*Lb*b - 2*Lb*f - 2*Lb*r*cos(phi))
		+ (Lb**2 - Lf**2 + b**2 - 2*b*f - 2*b*r*cos(phi) + f**2 + 2*f*r*cos(phi) + r**2 + z**2)
	)**2,
	4*Lb**2*z**2*(1 - c1**2)
	)
pprint(eq21)

print("\n\nEquation (22)")
eq22 = Eq(
	(
		c2 * (2*Lb*b - 2*Lb*f + 2*Lb*r*cos(phi + pi/3))
		+ (Lb**2 - Lf**2 + b**2 - 2*b*f + 2*b*r*cos(phi + pi/3) + f**2 - 2*f*r*cos(phi + pi/3) + r**2 + z**2)
	)**2,
	4*Lb**2*z**2*(1 - c2**2)
	)
pprint(eq22)

print("\n\nEquation (23)")
eq23 = Eq(
	(
		c3 * (2*Lb*b - 2*Lb*f + 2*Lb*r*cos(phi + pi/6))
		+ (Lb**2 - Lf**2 + b**2 - 2*b*f + 2*b*r*cos(phi + pi/6) + f**2 - 2*f*r*cos(phi + pi/6) + r**2 + z**2)
	)**2,
	4*Lb**2*z**2*(1 - c3**2)
	)
pprint(eq23)

'''

print("\n\nSolve (21) for c1:")
solutions_21 = solve(eq21, c1)
pprint(solutions_21)

print("\n\nSolve (22) for c2:")
solutions_22 = solve(eq22, c2)
pprint(solutions_22)

print("\n\nSolve (23) for c3:")
solutions_23 = solve(eq23, c3)
pprint(solutions_23)

'''










