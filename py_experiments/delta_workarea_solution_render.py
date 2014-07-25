#!/usr/bin/python
# -*- coding: utf-8 -*-
#

from pprint import pprint
from sympy import *

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


# координаты центров сфер
R1 = symbols('R1')

# радиусы окружностей - сечений сфер плоскостью
r1 = symbols('r1')

# радиус-вектор эффектора в плоскости z
# угол - относительно одного из плечей
r, phi1 = symbols('r phi1')

# уравнения для радиус-вектора положения эффектора
eq1 = Eq(r**2 - 2*r*R1*cos(phi1) + R1**2 - r1**2, 0)

print("\n\nEquations (1) with z, r, phi:")
pprint(eq1)

print("\n\nSolve (1) for r:")
solutions = solve(eq1, r)
pprint(solutions)




# координаты плоскости в которой находится эффектор
z = symbols('z')

# размеры частей дельта-робота
b, Lb, f, Lf = symbols('b Lb f Lf')

# угол отклонения плеча
theta1 = symbols('theta1')

# подставляем выражения для радиуса окружности и координаты окружности
for idx,s in enumerate(solutions):
	print("\n\nSolution #%d:" % idx)
	pprint(s.subs(r1, sqrt(Lf**2 - (z - Lb*sin(theta1))**2)).subs(R1, b-f+Lb*cos(theta1)))



# cos(theta1)
c = symbols('c')

# sin(theta1)
s = symbols('s')
s = sqrt(1 - c**2)

# b-f
d = symbols('d')

# уравнение для угла theta1
# R1 = d + Lb*c
# r1**2 = Lf**2 - (z - Lb*s)**2
expr1 = r**2 - 2*r*R1*cos(phi1) + R1**2 - r1**2
expr2 = expr1.subs(r1, sqrt(Lf**2 - (z - Lb*s)**2)).subs(R1, d + Lb*c)
expr3 = expr2.expand().simplify().collect(c)

print("\n\nExpression (2) with c = cos(theta):")
pprint(expr3)














