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


Alfa = [0, -2*pi/3, 2*pi/3]


def _r_valid (b, f, Lb, Lf, z, phi, r, alfa0):

	valid = 0

	B = (b-f)**2 - 2*r*(b-f) + Lb**2 + r**2 - Lf**2 + z**2
	C = 2*z*Lb

	for alfa in Alfa:
		if alfa != alfa0:
			# у нас есть вектор эффектора - находим радиусы двух других окружностей
			# и проверяем валидность получившихся соответствующих theta
			A = 2*(b-f)*Lb - 2*r*Lb*cos(phi + alfa)

			D = C**2 * (A**2 - B**2 + C**2)

			if D >= 0:
				cos_theta = [
					(-A*B + sqrt(D))/(A**2 + C**2),
					-(A*B + sqrt(D))/(A**2 + C**2)
					]
				print(r, cos_theta)

				if (cos_theta[0] >= 0 and cos(pi/3) <= cos_theta[0]) or (cos_theta[1] >= 0 and cos(pi/3) <= cos_theta[1]):
					valid += 1

	print(valid)
	return valid == 2


# inverse kinematics
# helper functions, calculates angle theta1 (for YZ-pane)
def delta_calcAngleYZ(x0, y0, z0, f, e, rf, re) :

	y1 = -0.5 * 0.57735 * f # f/2 * tg 30
	y0 -= 0.5 * 0.57735 * e    # shift center to edge

	# z = a + b*y
	a = (x0*x0 + y0*y0 + z0*z0 +rf*rf - re*re - y1*y1)/(2*z0)
	b = (y1-y0)/z0

	# discriminant
	d = -(a+b*y1)*(a+b*y1)+rf*(b*b*rf+rf)

	if d < 0:
		return (False, 0) # non-existing point

	yj = (y1 - a*b - sqrt(d))/(b*b + 1) # choosing outer point
	zj = a + b*yj

	theta = 180.0*atan(-zj/(y1 - yj))/pi + (180.0 if yj>y1 else 0.0)

	return (True, theta)


def delta_calcInverse(x0, y0, z0, f, e, rf, re) :

	theta1 = 0
	theta2 = 0
	theta3 = 0

	status, theta1 = delta_calcAngleYZ(x0, y0, z0, f, e, rf, re)

	if status:
		status, theta2 = delta_calcAngleYZ(x0*cos(2*pi/3) + y0*sin(2*pi/3), y0*cos(2*pi/3)-x0*sin(2*pi/3), z0, f, e, rf, re)  # rotate coords to +120 deg
	if status:
		status, theta3 = delta_calcAngleYZ(x0*cos(2*pi/3) - y0*sin(2*pi/3), y0*cos(2*pi/3)+x0*sin(2*pi/3), z0, f, e, rf, re)  # rotate coords to -120 deg

	return (status, theta1, theta2, theta3)



def r_valid (b, f, Lb, Lf, z, phi, r):

	x = r*cos(phi)
	y = r*sin(phi)

	result = delta_calcInverse(x, y, z, b*2/tan(pi/6), f*2/tan(pi/6), Lb, Lf)

	return result[0] and abs(result[1]) <= 60 and abs(result[2]) <= 60 and abs(result[3]) <= 60



# Theta - list of two borders for thetai
def max_r (b, f, Lb, Lf, z, phi, Theta):

	r_values = []

	for theta in Theta:

		for alfa in Alfa:
			result = r_solution(b, f, Lb, Lf, theta, z, phi + alfa)

			if result:
				for r in result:
					if r >= 0 and r_valid(b, f, Lb, Lf, z, phi, r):
						r_values.append(r)

	if len(r_values) > 0:
		return max(r_values)
	else:
		return None


B = 125
F = 35
LB = 120
LF = 325


x_data = []
y_data = []
z_data = []

for z in range(-430, -170, 5):
	for p in range(0, 73):
		phi = p*pi/36
		r = max_r(B, F, LB, LF, z, phi, [-pi/3, pi/3])
		if r:
			x = r*cos(phi)
			y = r*sin(phi)
			x_data.append(x)
			y_data.append(y)
			z_data.append(z)

import numpy as np

X = np.array(x_data)
Y = np.array(y_data)
Z = np.array(z_data)


from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

'''

Phi = np.linspace(0, 2 * np.pi, 100)
Z_val = np.linspace(-400, 0, 100)


def R (Phi, Z):
	data = []
	for z in Z:
		for phi in Phi:
			data.append(max_r(B, F, LB, LF, z, phi, [-pi/3, pi/3]))
	return np.array(data)



X = np.outer(np.cos(Phi), np.abs(Z_val)*np.sin(Phi))
Y = np.outer(np.sin(Phi), np.abs(Z_val)*np.cos(Phi))
Z = np.outer(np.ones(100), Z_val)


'''


ax.plot_wireframe(X, Y, Z,  rstride=4, cstride=4, color='b')

plt.show()



