#!/usr/bin/python
# -*- coding: utf-8 -*-
#

from pprint import pprint
from sympy import *

init_printing(use_unicode=True, use_latex=False)

# пересечение трёх сфер одинакового радиуса

x, y, z, r = symbols('x y z, r')

x1, y1, z1 = symbols('x1 y1 z1')
x2, y2, z2 = symbols('x2 y2 z2')
x3, y3, z3 = symbols('x3 y3 z3')

r1_p2 = (x - x1)**2 + (y - y1)**2 + (z - z1)**2
r2_p2 = (x - x2)**2 + (y - y2)**2 + (z - z2)**2
r3_p2 = (x - x3)**2 + (y - y3)**2 + (z - z3)**2

eq_1 = Eq(r1_p2, r**2)
eq_2 = Eq(r2_p2, r**2)
eq_3 = Eq(r3_p2, r**2)

print("\n\n(1):")
pprint(eq_1)
print("\n\n(2):")
pprint(eq_2)
print("\n\n(3):")
pprint(eq_3)

print("\n\nsolve (1),(2),(3) for x, y, z:")
solutions = solve([eq_1, eq_2, eq_3], [x, y, z])

pprint(solutions)




