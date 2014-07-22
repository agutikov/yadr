#!/usr/bin/python
# -*- coding: utf-8 -*-
#

from pprint import pprint
from math import *


def Ri (b, f, Lb, thetai):
	return b - f + Lb*cos(thetai)

def ri_p2 (Lf, z, Lb, thetai):
	return Lf**2 - (z - Lb*sin(thetai))**2


def r_solution (b, f, Lb, Lf, thetai, z, phii):
	D = (Ri(b, f, Lb, thetai)**2)*(cos(phii)**2 - 1) + ri_p2(Lf, z, Lb, thetai)
	if D >= 0:
		a = Ri(b, f, Lb, thetai)*cos(phii)
		return [-a - sqrt(D), -a + sqrt(D)]
	else:
		return None


# Theta - list of two borders for thetai
def max_r (b, f, Lb, Lf, z, phii, Theta):

	Phi = [phii, 2*pi/3 - phii, 4*pi/3 - phii]

	r_values_max = []

	for theta in Theta:
		r_values_min = []

		for phi in Phi:
			r_val = r_solution(b, f, Lb, Lf, theta, z, phi)
			if r_val:
				r_values_min += filter(lambda x: x > 0, r_val)

		if len(r_values_min) > 0:
			r_values_max.append(min(r_values_min))

	if len(r_values_max) > 0:
		return max(r_values_max)
	else:
		return None


B = 130
F = 50
LB = 120
LF = 320


x_data = []
y_data = []
z_data = []

for z in range(-500, 0, 10):
	for p in range(0, 37):
		phi = p*pi/18
		r = max_r(B, F, LB, LF, z, phi, [-pi/3, pi/3])
		if r:
			x = r*cos(phi)
			y = r*sin(phi)
			x_data.append(x)
			y_data.append(y)
			z_data.append(z)



from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y, Z = x_data, y_data, z_data
ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)

plt.show()








