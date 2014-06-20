#!/usr/bin/python

# http://forums.trossenrobotics.com/tutorials/introduction-129/delta-robot-kinematics-3276/

import sys
import io
from pprint import pprint
import math



# robot geometry
# (look at pics above for explanation)
e = 115.0     # end effector
f = 457.3     # base
re = 232.0
rf = 112.0

# trigonometric constants
sqrt3 = math.sqrt(3.0)
sin120 = sqrt3/2.0
cos120 = -0.5
tan60 = sqrt3
sin30 = 0.5
tan30 = 1/sqrt3

dtr = math.pi/180.0
t = (f-e)*tan30/2

# forward kinematics: (theta1, theta2, theta3) -> (x0, y0, z0)
# returned status: 0=OK, -1=non-existing position
def delta_calcForward(theta1, theta2, theta3) :

	theta1 *= dtr
	theta2 *= dtr
	theta3 *= dtr

	y1 = -(t + rf*math.cos(theta1))
	z1 = -rf*math.sin(theta1)

	y2 = (t + rf*math.cos(theta2))*sin30
	x2 = y2*tan60
	z2 = -rf*math.sin(theta2)

	y3 = (t + rf*math.cos(theta3))*sin30
	x3 = -y3*tan60
	z3 = -rf*math.sin(theta3)

	dnm = (y2-y1)*x3-(y3-y1)*x2

	w1 = y1*y1 + z1*z1
	w2 = x2*x2 + y2*y2 + z2*z2
	w3 = x3*x3 + y3*y3 + z3*z3

	# x = (a1*z + b1)/dnm
	a1 = (z2-z1)*(y3-y1)-(z3-z1)*(y2-y1)
	b1 = -((w2-w1)*(y3-y1)-(w3-w1)*(y2-y1))/2.0

	# y = (a2*z + b2)/dnm
	a2 = -(z2-z1)*x3+(z3-z1)*x2
	b2 = ((w2-w1)*x3 - (w3-w1)*x2)/2.0

	# a*z^2 + b*z + c = 0
	a = a1*a1 + a2*a2 + dnm*dnm
	b = 2*(a1*b1 + a2*(b2-y1*dnm) - z1*dnm*dnm)
	c = (b2-y1*dnm)*(b2-y1*dnm) + b1*b1 + dnm*dnm*(z1*z1 - re*re)

	# discriminant
	d = b*b - 4.0*a*c
	if d < 0:
		return (False, 0,0,0) # non-existing point

	z0 = -0.5*(b+math.sqrt(d))/a
	x0 = (a1*z0 + b1)/dnm
	y0 = (a2*z0 + b2)/dnm

	return (True, x0, y0, z0)


# inverse kinematics
# helper functions, calculates angle theta1 (for YZ-pane)
def delta_calcAngleYZ(x0, y0, z0) :

	y1 = -0.5 * 0.57735 * f # f/2 * tg 30
	y0 -= 0.5 * 0.57735 * e    # shift center to edge

	# z = a + b*y
	a = (x0*x0 + y0*y0 + z0*z0 +rf*rf - re*re - y1*y1)/(2*z0)
	b = (y1-y0)/z0

	# discriminant
	d = -(a+b*y1)*(a+b*y1)+rf*(b*b*rf+rf)

	if d < 0:
		return (False, 0) # non-existing point

	yj = (y1 - a*b - math.sqrt(d))/(b*b + 1) # choosing outer point
	zj = a + b*yj

	theta = 180.0*math.atan(-zj/(y1 - yj))/math.pi + (180.0 if yj>y1 else 0.0)

	return (True, theta)



# inverse kinematics: (x0, y0, z0) -> (theta1, theta2, theta3)
# returned status: 0=OK, -1=non-existing position
def delta_calcInverse(x0, y0, z0) :

	theta1 = 0
	theta2 = 0
	theta3 = 0

	status, theta1 = delta_calcAngleYZ(x0, y0, z0)

	if status:
		status, theta2 = delta_calcAngleYZ(x0*cos120 + y0*sin120, y0*cos120-x0*sin120, z0)  # rotate coords to +120 deg
	if status:
		status, theta3 = delta_calcAngleYZ(x0*cos120 - y0*sin120, y0*cos120+x0*sin120, z0)  # rotate coords to -120 deg

	return (status, theta1, theta2, theta3)



# print("  a   b   c   :   x    y    z")
# print("-----------------------------")

rng = list(range(-60, 70, 10))
irng = list(reversed(rng))

a = -60
b = -60

for a in rng:
	xyz = delta_calcForward(a, b, b)[1:]
#	print(("%3d %3d %3d   :" % (a, b, b)) + "%4.1d %4.1d %4.1d" % xyz)

a = 60

for b in rng:
	xyz = delta_calcForward(a, b, b)[1:]
#	print(("%3d %3d %3d   :" % (a, b, b)) + "%4.1d %4.1d %4.1d" % xyz)

b = 60

for a in irng:
	xyz = delta_calcForward(a, b, b)[1:]
#	print(("%3d %3d %3d   :" % (a, b, b)) + "%4.1d %4.1d %4.1d" % xyz)

a = -60

for b in irng:
	xyz = delta_calcForward(a, b, b)[1:]
#	print(("%3d %3d %3d   :" % (a, b, b)) + "%4.1d %4.1d %4.1d" % xyz)


list_all = []

start = -60
stop = 60
d = 3
rng = range(start, stop + d, d)

for a in rng:
	for b in rng:
		for c in rng:
			xyz = delta_calcForward(a, b, c)[1:]
			list_all.append(xyz)
			# print("%f %f %f" % xyz)

sorted_list = sorted(list_all, key=lambda a: a[2])

for t in sorted_list:
	print("%f %f %f" % t)





