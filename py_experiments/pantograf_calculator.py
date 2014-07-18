#!/usr/bin/python


import sys
import io
from pprint import pprint
# from math import sin,cos,floor,ceil,asin,acos
from sympy import *
from mpmath import degrees,radians
import pickle



init_printing(use_unicode=True, use_latex=False)


angles = [0, 30, 45, 60, 90]

#sizes = [(1, 1, 2*sqrt(2)), (1, 1, 3), (1, 1, 4), (1, 1, 10)]
sizes = [(1, 1, 4)]


filename = sys.argv[1]


a1, b1, s, l, r, x, y = symbols('a1 b1 s l r x y')



eq = pickle.load(open(filename, 'rb'))



# pprint(eq)


for A in angles:
	for B in angles:
		for D in sizes:
			print("\n", "s =", D[0], "r =", D[1], "l =", D[2], "a1 =", A, "b1 =", B,
			"x =", eq[0].subs(a1, A).subs(b1, B).subs(s, D[0]).subs(l, D[2]).subs(r, D[1]).evalf(4),
			"y =", eq[1].subs(a1, A).subs(b1, B).subs(s, D[0]).subs(l, D[2]).subs(r, D[1]).evalf(4)
			)









































