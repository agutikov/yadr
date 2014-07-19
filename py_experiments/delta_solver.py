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
	X,Y,Z - координаты центра еффектора
	b - расстояние от базы до оси руки
	lb - длинна руки
	f - расстояние от центра еффектора до точки крепления тяги
	lf - длинна тяги

	первое плечо расположено вдоль оси х, второе в сторону оси y, третье - обратно оси y.
	углы поворота плеч - theta1, theta2, theta3 - положительные вверх, отрицательные вниз

	координаты крепления осей плеч к базе, они-же векторы из центра базы к осям:
	1) x1 = b,        y1 = 0,        z1 = 0
	2) x2 = -b*sin30, y2 = b*cos30,  z2 = 0
	3) x3 = -b*sin30, y3 = -b*cos30, z3 = 0

	векторы плеч:
	1) x1 = lb*cos(theta1),        y1 = 0,                     z1 = lb*sin(theta1)
	2) x2 = -lb*cos(theta2)*sin30, y2 = lb*cos(theta2)*cos30,  z2 = lb*sin(theta2)
	3) x3 = -lb*cos(theta3)*sin30, y3 = -lb*cos(theta3)*cos30, z3 = lb*sin(theta3)

	векторы от точек крепелния тяг на эффекторе к его центру:
	1) x1 = -f,        y1 = 0,        z1 = 0
	2) x2 = f*sin30,   y2 = -f*cos30, z2 = 0
	3) x3 = f*sin30,   y3 = f*cos30,  z3 = 0


	считаем прямую кинематику:
		http://forums.trossenrobotics.com/tutorials/introduction-129/delta-robot-kinematics-3276/
		Forward kinematics

	1) складываем соответствующие тройки векторов - получаем три точки (или три вектора)
		полученные координаты точек: (x1, y1, z1), (x2, y2, z2), (x3, y3, z3)

	2) в этих точках помещаем сферы с радиусом равным длинне дельты
		получаем систему квадратных уравнений
		(X - x1)**2 + (Y - y1)**2 + (Z - z1)**2 = lf**2
		(X - x2)**2 + (Y - y2)**2 + (Z - z2)**2 = lf**2
		(X - x3)**2 + (Y - y3)**2 + (Z - z3)**2 = lf**2

	3) нижнее пересечение этих трех сфер находится в центре эффектора

'''


b, lb, f, lf = symbols('b lb f lf')
theta1, theta2, theta3 = symbols('theta1 theta2 theta3')

X1, X2, X3 = symbols('X1 X2 X3')
Y1, Y2, Y3 = symbols('Y1 Y2 Y3')
Z1, Z2, Z3 = symbols('Z1 Z2 Z3')

X1 = b + lb*cos(theta1) - f
X2 = -b*sin(pi/6) + -lb*cos(theta2)*sin(pi/6) + f*sin(pi/6)
X3 = -b*sin(pi/6) + -lb*cos(theta3)*sin(pi/6) + f*sin(pi/6)

Y1 = 0
Y2 = b*cos(pi/6) + lb*cos(theta2)*cos(pi/6) + -f*cos(pi/6)
Y3 = -b*cos(pi/6) + -lb*cos(theta3)*cos(pi/6) + f*cos(pi/6)

Z1 = lb*sin(theta1)
Z2 = lb*sin(theta2)
Z3 = lb*sin(theta3)

print("\n\nX1 =")
pprint(X1)
print("\n\nX2 =")
pprint(X2)
print("\n\nX3 =")
pprint(X3)

print("\n\nY1 =")
pprint(Y1)
print("\n\nY2 =")
pprint(Y2)
print("\n\nY3 =")
pprint(Y3)

print("\n\nZ1 =")
pprint(X1)
print("\n\nZ2 =")
pprint(Z2)
print("\n\nZ3 =")
pprint(Z3)


X, Y, Z = symbols('X Y Z')

x1, y1, z1 = symbols('x1 y1 z1')
x2, y2, z2 = symbols('x2 y2 z2')
x3, y3, z3 = symbols('x3 y3 z3')

# радиусы в квадрате (radius#_power2)
# r1_p2 = (X - x1)**2 + (Y - y1)**2 + (Z - z1)**2
# y1 == 0
r1_p2 = (X - x1)**2 + Y**2 + (Z - z1)**2
r2_p2 = (X - x2)**2 + (Y - y2)**2 + (Z - z2)**2
r3_p2 = (X - x3)**2 + (Y - y3)**2 + (Z - z3)**2

eq_1 = Eq(r1_p2, lf**2)
eq_2 = Eq(r2_p2, lf**2)
eq_3 = Eq(r3_p2, lf**2)

print("\n\n(1):")
pprint(eq_1)
print("\n\n(2):")
pprint(eq_2)
print("\n\n(3):")
pprint(eq_3)


'''
	Sympy сам оказался не в состоянии решит систему квадратных уравнений...
	Надо ему помоч.

	(X - x1)^2 + (Y - y1)^2 + (Z - z1)^2 = lf^2
	(X - x2)^2 + (Y - y2)^2 + (Z - z2)^2 = lf^2
	(X - x3)^2 + (Y - y3)^2 + (Z - z3)^2 = lf^2

	X^2 - 2x1*X + Y^2 - 2y1*Y + X^2 - 2z1*Z = lf^2 - (x1^2 + y1^2 + z1^2)
	X^2 - 2x2*X + Y^2 - 2y2*Y + X^2 - 2z2*Z = lf^2 - (x2^2 + y2^2 + z2^2)
	X^2 - 2x3*X + Y^2 - 2y3*Y + X^2 - 2z3*Z = lf^2 - (x3^2 + y3^2 + z3^2)

	wi = xi^2 + yi^2 + zi^2

	X^2 + Y^2 + X^2 - 2x1*X - 2y1*Y - 2z1*Z = lf^2 - w1 (1)
	X^2 + Y^2 + X^2 - 2x2*X - 2y2*Y - 2z2*Z = lf^2 - w2 (2)
	X^2 + Y^2 + X^2 - 2x3*X - 2y3*Y - 2z3*Z = lf^2 - w3 (3)

	(1) - (2)
	(x2 - x1)*X + (y2 - y1)*Y + (z2 - z1)*Z = (w2 - w1)/2

	(1) - (3)
	(x3 - x1)*X + (y3 - y1)*Y + (z3 - z1)*Z = (w3 - w1)/2


	-----------------------------------------------------
	Т.к. первая рука расположена вдоль оси x - то y1 == 0,
	а следовательно:

	(X - x1)^2 + Y^2 + (Z - z1)^2 = lf^2

	X^2 - 2x1*X + Y^2 + X^2 - 2z1*Z = lf^2 - (x1^2 + z1^2)

	X^2 + Y^2 + X^2 - 2x1*X - 2z1*Z = lf^2 - w1 (1)

	(1) - (2)
	(x2 - x1)*X + y2*Y + (z2 - z1)*Z = (w2 - w1)/2

	(1) - (3)
	(x3 - x1)*X + y3*Y + (z3 - z1)*Z = (w3 - w1)/2

'''

print("\n", "="*100)

W1, W2, W3 = symbols('W1 W2 W3')

W1 = x1**2 + y1**2 + z1**2
W2 = x2**2 + y2**2 + z2**2
W3 = x3**2 + y3**2 + z3**2

pprint("\n\nW1 =")
pprint(W1)
pprint("\n\nW2 =")
pprint(W2)
pprint("\n\nW3 =")
pprint(W3)

w1, w2, w3 = symbols('w1 w2 w3')

eq_4 = Eq((x2 - x1)*X + y2*Y + (z2 - z1)*Z, (w2 - w1)/2)
eq_5 = Eq((x3 - x1)*X + y3*Y + (z3 - z1)*Z, (w3 - w1)/2)

print("\n\n(4) = (1) - (2):")
pprint(eq_4)
print("\n\n(5) = (1) - (3):")
pprint(eq_5)


print("\n\nsolving (4),(5) for X and Y:")
solutions_XY = solve([eq_4, eq_5], [X, Y])
pprint(solutions_XY)


eq_X = Eq(X, solutions_XY[X])

eq_Y = Eq(Y, solutions_XY[Y])

print("\n\n(6) - equation for X(Z):")
pprint(eq_X)
print("\n\n(7) - equation for Y(Z):")
pprint(eq_Y)


# here look at equations for X and Y and redefine expressions as X = a1*Z + b1, Y = a2*Z + b2
# quit()

A1, B1, A2, B2, D = symbols('A1 B1 A2 B2 D')

D = (y2*(x1 - x3) - y3*(x1 - x2))

A1 = (y2*(z3 - z1) + y3*(z1 - z2)) / D

B1 = (w1*(y2 - y3) + w2*y3 - w3*y2) / (2*D)

A2 = ((x1 - x2)*(z3 - z1) + (x1 - x3)*(z1 - z2)) / D

B2 = ((x1 - x2)*(w1 - w3) + (x1 - x3)*(-w1 + w2)) / (2*D)

print("\n\nD = ")
pprint(D)
print("\n\nA1 = ")
pprint(A1)
print("\n\nB1 = ")
pprint(B1)
print("\n\nA2 = ")
pprint(A2)
print("\n\nB2 = ")
pprint(B2)


a1, b1, a2, b2, d = symbols('a1 b1 a2 b2 d')

print("\n\nX =")
exp_X_simple = a1*Z + b1
pprint(exp_X_simple)

print("\n\nY =")
exp_Y_simple = a2*Z + b2
pprint(exp_Y_simple)



print("\n\nsubstitude X and Y into (1):")
exp1 = r1_p2.subs(X, exp_X_simple).subs(Y, exp_Y_simple)
pprint(exp1)



print("\n\nexpand:")
exp2 = expand(exp1)
pprint(exp2)

print("\n\ncollect:")
exp3 = collect(exp2, Z)
pprint(exp3)

print("\n\nZ^2 coefficient:")
z2_coeff = exp3.coeff(Z, 2)
pprint(z2_coeff)

print("\n\nZ coefficient:")
z1_coeff = exp3.coeff(Z, 1)
pprint(z1_coeff)

print("\n\nconst:")
z0_coeff = exp3.coeff(Z, 0)
pprint(z0_coeff)

eq_Z_final_simple = Eq(z2_coeff*Z**2 + z1_coeff*Z + z0_coeff - lf**2, 0)
print("\n\n(8):")
pprint(eq_Z_final_simple)


print("\n\nsolving (8) for Z")
solutions_Z_final = solve(eq_Z_final_simple, Z)

print("\n\nTOTAL: %d Z solutions:" % len(solutions_Z_final))
pprint(solutions_Z_final)

#quit()
# fist solution is with -sqrt(discreminant) - so use first folution

z_sol_w = solutions_Z_final[0]

print("\n\nZ =")
pprint(z_sol_w)

print("\n\nsubstitude Z into (6):")
eq_X_final = eq_X.subs(Z, z_sol_w)
pprint(eq_X_final)

print("\n\nsolve (6) for X")
x_sol_w = solve(eq_X_final, X)[0]

print("\n\nX =")
pprint(x_sol_w)

print("\n\nsubstitude Z into (7):")
eq_Y_final = eq_Y.subs(Z, z_sol_w)
pprint(eq_Y_final)

print("\n\nsolve (7) for Y")
y_sol_w = solve(eq_Y_final, Y)[0]

print("\n\nY =")
pprint(y_sol_w)

print("\n\nsubstitude a1, a2, b1, b2, d")
x_sol_ab = x_sol_w.subs(a1, A1).subs(a2, A2).subs(b1, B1).subs(b2, B2).subs(d, D)
y_sol_ab = y_sol_w.subs(a1, A1).subs(a2, A2).subs(b1, B1).subs(b2, B2).subs(d, D)
z_sol_ab = z_sol_w.subs(a1, A1).subs(a2, A2).subs(b1, B1).subs(b2, B2).subs(d, D)

print("\n\nX =")
pprint(x_sol_ab)
print("\n\nY =")
pprint(y_sol_ab)
print("\n\nZ =")
pprint(z_sol_ab)

print("\n\nsubstitude w1, w2, w3")
x_sol = x_sol_ab.subs(w1, W1).subs(w2, W2).subs(w3, W3)
y_sol = y_sol_ab.subs(w1, W1).subs(w2, W2).subs(w3, W3)
z_sol = z_sol_ab.subs(w1, W1).subs(w2, W2).subs(w3, W3)

print("\n\nX =")
pprint(x_sol)
print("\n\nY =")
pprint(y_sol)
print("\n\nZ =")
pprint(z_sol)


print("\n\nsubstitude x1,x2,x3, y1,y2,y3, z1,z2,z3")
x_sol_real = x_sol.subs(x1, X1).subs(x2, X2).subs(x3, X3).subs(y1, Y1).subs(y2, Y2).subs(y3, Y3).subs(z1, Z1).subs(z2, Z2).subs(z3, Z3)
y_sol_real = y_sol.subs(x1, X1).subs(x2, X2).subs(x3, X3).subs(y1, Y1).subs(y2, Y2).subs(y3, Y3).subs(z1, Z1).subs(z2, Z2).subs(z3, Z3)
z_sol_real = z_sol.subs(x1, X1).subs(x2, X2).subs(x3, X3).subs(y1, Y1).subs(y2, Y2).subs(y3, Y3).subs(z1, Z1).subs(z2, Z2).subs(z3, Z3)

print("\n\nX =")
pprint(x_sol_real)
print("\n\nY =")
pprint(y_sol_real)
print("\n\nZ =")
pprint(z_sol_real)





