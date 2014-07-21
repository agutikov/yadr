#!/usr/bin/python
# -*- coding: utf-8 -*-
#

from pprint import pprint
from sympy import *

init_printing(use_unicode=True, use_latex=False)

# пересечение трёх окружностей разных радиусов

x, y = symbols('x y')
r1, r2, r3 = symbols('r1 r2 r3')

x1, y1 = symbols('x1 y1')
x2, y2 = symbols('x2 y2')
x3, y3 = symbols('x3 y3')

r1_p2 = (x - x1)**2 + (y - y1)**2
r2_p2 = (x - x2)**2 + (y - y2)**2
r3_p2 = (x - x3)**2 + (y - y3)**2

eq_1 = Eq(r1_p2, r1**2)
eq_2 = Eq(r2_p2, r2**2)
eq_3 = Eq(r3_p2, r3**2)

print("\n\n(1):")
pprint(eq_1)
print("\n\n(2):")
pprint(eq_2)
print("\n\n(3):")
pprint(eq_3)

print("\n\nsolve (1),(2),(3) for x, y:")
solutions = solve([eq_1, eq_2], [x, y])


for s in solutions:
	print("\n\n")
	print("="*100)
	print("\n\nX = ")
	pprint(s[0])
	print("\n\nY = ")
	pprint(s[1])


