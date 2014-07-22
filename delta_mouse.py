#!/usr/bin/python

import sys
import os
import io
import time
from pprint import pprint
from optparse import OptionParser
import pygame
# import pygame.freetype
from math import *
import serial

# TODO: config file woth delta settings: base and affecrot radius, arm and delta length, foreach servo: start pwm, angle coefficient, max and min angles




usage_text = "Usage: %prog -D <serial_port>\n"

opt_parser = OptionParser(usage=usage_text)

opt_parser.add_option('-D', '--device',
		      help="Serial port device file.",
		      action='store', type="string", dest="device_filename")

opt_parser.add_option("-t", "--test",
                  action="store_true", dest="run_test", default=False,
                  help="just run buit-in test")

opt_values, args = opt_parser.parse_args()

opts = vars(opt_values)

# pprint(opts)
# pprint(args)


class delta_kinematics:
# http://forums.trossenrobotics.com/tutorials/introduction-129/delta-robot-kinematics-3276/

	# trigonometric constants
	sqrt3 = sqrt(3.0)
	sin120 = sqrt3/2.0
	cos120 = -0.5
	tan60 = sqrt3
	sin30 = 0.5
	tan30 = 1/sqrt3

	dtr = pi/180.0

	def __init__(self, r_base, r_aff, l_arm, l_delta):
		self.e = 2*self.sqrt3*r_aff     # end effector
		self.f = 2*self.sqrt3*r_base     # base
		self.re = l_delta
		self.rf = l_arm

		self.t = (self.f-self.e)*self.tan30/2

	# forward kinematics: (theta1, theta2, theta3) -> (x0, y0, z0)
	# returned status: 0=OK, -1=non-existing position
	def delta_calcForward (self, theta1, theta2, theta3) :

		theta1 *= self.dtr
		theta2 *= self.dtr
		theta3 *= self.dtr

		y1 = -(self.t + self.rf*cos(theta1))
		z1 = -self.rf*sin(theta1)

		y2 = (self.t + self.rf*cos(theta2))*self.sin30
		x2 = y2*self.tan60
		z2 = -self.rf*sin(theta2)

		y3 = (self.t + self.rf*cos(theta3))*self.sin30
		x3 = -y3*self.tan60
		z3 = -self.rf*sin(theta3)

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
		c = (b2-y1*dnm)*(b2-y1*dnm) + b1*b1 + dnm*dnm*(z1*z1 - self.re**2)

		# discriminant
		d = b*b - 4.0*a*c
		if d < 0:
			return (False, 0,0,0) # non-existing point

		z0 = -0.5*(b+sqrt(d))/a
		x0 = (a1*z0 + b1)/dnm
		y0 = (a2*z0 + b2)/dnm

		return (True, int(x0), int(y0), int(z0))

	# inverse kinematics
	# helper functions, calculates angle theta1 (for YZ-pane)
	def _delta_calcAngleYZ (self, x0, y0, z0) :

		y1 = -0.5 * 0.57735 * self.f # f/2 * tg 30
		y0 -= 0.5 * 0.57735 * self.e    # shift center to edge

		# z = a + b*y
		a = (x0*x0 + y0*y0 + z0*z0 +self.rf**2 - self.re**2 - y1*y1)/(2*z0)
		b = (y1-y0)/z0

		# discriminant
		d = -(a+b*y1)*(a+b*y1)+self.rf*(b*b*self.rf+self.rf)

		if d < 0:
			return (False, 0) # non-existing point

		yj = (y1 - a*b - sqrt(d))/(b*b + 1) # choosing outer point
		zj = a + b*yj

		theta = 180.0*atan(-zj/(y1 - yj))/pi + (180.0 if yj>y1 else 0.0)

		return (True, theta)

	# inverse kinematics: (x0, y0, z0) -> (theta1, theta2, theta3)
	# returned status: 0=OK, -1=non-existing position
	def delta_calcInverse (self, x0, y0, z0) :

		theta1 = 0
		theta2 = 0
		theta3 = 0

		status, theta1 = self._delta_calcAngleYZ(x0, y0, z0)

		if status:
			status, theta2 = self._delta_calcAngleYZ(x0*self.cos120 + y0*self.sin120, y0*self.cos120-x0*self.sin120, z0)  # rotate coords to +120 deg
		if status:
			status, theta3 = self._delta_calcAngleYZ(x0*self.cos120 - y0*self.sin120, y0*self.cos120+x0*self.sin120, z0)  # rotate coords to -120 deg

		return (status, int(theta1), int(theta2), int(theta3))

class point:
	def __init__ (self, point_tuple):
		self.x, self.y, self.z = point_tuple

	def __add__ (self, p):
		return point((self.x + p.x, self.y + p.y, self.z + p.z))

	def __sub__ (self, p):
		return point((self.x - p.x, self.y - p.y, self.z - p.z))

	def tuple (self):
		return (self.x, self.y, self.z)

	def scal_xy(self, b):
		return self.x*b.x + self.y*b.y

	def norm_xy (self):
		s = sqrt(self.scal_xy(self))
		if s != 0:
			self.x /= s
			self.y /= s
		else:
			self.x = 0
			self.y = 0

	def mul_xy (self, k):
		self.x *= k
		self.y *= k



kinematics = delta_kinematics(120, 35, 125, 325)

angle_max = 60
angle_min = -60

work_R = 120
work_bootom = -350
work_H = 200
print("Work area: r=%d, floor=%d, h=%d" % (work_R, work_bootom, work_H))

# starting point in work coordinates
work_start = point((0, 0, 100))

# convert coordinates from working into delta (shift start down to work_bootom)
def convert_point (p):
	return p + point((0, 0, work_bootom))

def sign (x):
	return 1 if x >= 0 else -1

# do not go out of work coordinates
# call before convert
def point_bounds (p):
	result = point(p.tuple())
	if result.z < 0:
		result.z = 0
	if result.z > work_H:
		result.z = work_H
#	if abs(result.y) >= work_R:
#		result.y = sign(result.y) * (work_R-1)

	if (result.x**2 + result.y**2) > work_R**2 :
#		result.x = sign(result.x)*int(sqrt(work_R**2 - result.y**2))
		result.norm_xy()
		result.mul_xy(work_R)

	return result


duty_centers = [1400, 1500, 1500]
duty_multipy = [10, 10, 10]

# convert angles into pwm duty cycle length in microseconds
def angles2duty (a_t):
	return (a_t[0]*duty_multipy[0] + duty_centers[0],
	 a_t[1]*duty_multipy[1] + duty_centers[1],
	 a_t[2]*duty_multipy[2] + duty_centers[2])

# do not go out of allowed angles
def angles_bounds (a_t):
	return (angle_max if a_t[0] > angle_max else (angle_min if a_t[0] < angle_min else a_t[0]),
	 angle_max if a_t[1] > angle_max else (angle_min if a_t[1] < angle_min else a_t[1]),
	 angle_max if a_t[2] > angle_max else (angle_min if a_t[2] < angle_min else a_t[2]))


# intial condition
work_current_point = point((0,0,0))
delta_current_point = point((0,0,0))
delta_current_angles = (0,0,0)
delta_current_pwm = (0,0,0)


# convert delta point into angles
def point2angles (delta_point):
	global delta_current_angles
	kin = kinematics.delta_calcInverse(delta_point.x, delta_point.y, delta_point.z)
	if kin[0]:
		angles = kin[1:]
		delta_current_angles = angles_bounds(angles)
'''
	else:
		print("point2angles: kinematics fail")
		print("delta_point:")
		pprint(delta_point.tuple())
		print("kinematics result:")
		pprint(kin)
'''

def delta_reset():
	global work_current_point
	global delta_current_point
	global delta_current_pwm
	work_current_point = point(work_start.tuple())
	work_current_point = point_bounds(work_current_point)
	delta_current_point = convert_point(work_current_point)
	point2angles(delta_current_point)
	delta_current_pwm = angles2duty(delta_current_angles)

delta_reset()

def delta_update():
	global work_current_point
	global delta_current_point
	global delta_current_pwm
	work_current_point = point_bounds(work_current_point)
	delta_current_point = convert_point(work_current_point)
	point2angles(delta_current_point)
	delta_current_pwm = angles2duty(delta_current_angles)

print("work start point:")
pprint(work_current_point.tuple())
print("delta start point:")
pprint(delta_current_point.tuple())
print("delta start angles:")
pprint(delta_current_angles)
print("delta start pwm:")
pprint(delta_current_pwm)


if opts["device_filename"]:
	port = serial.Serial(port=opts["device_filename"],
#			baudrate=19200, # arduino
			baudrate=115200, # stm32vl discovery
			timeout=0,
			bytesize=serial.EIGHTBITS,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			xonxoff=False,
			rtscts=False,
			dsrdtr=False
			)

	try:
		print("opening " + opts["device_filename"])
	#	port.open()
	except serial.SerialException as e:
		pprint(e)
		exit(-3)

	if not port.isOpen():
		print("Can't open " + opts["device_filename"])
		exit(-2)



def delta_write():
#	pprint(delta_current_pwm)
#	cmd = "%df%dg%dh" % delta_current_pwm
	# for stm32 usart terminal implementation send CR byte
	# minicom works because it opens serial port in terminal mode
	cmd = "pwm duty %d %d %d\r" % delta_current_pwm
#	pprint(cmd)
	if opts["device_filename"]:
		port.write(bytes(cmd, 'UTF-8'))
#		pprint(port.read())

if opts["run_test"]:
	print("Start test")

	if len(args) == 0:
		delta_update()
		delta_write()
		time.sleep(1)

		for z in reversed(range(15, work_current_point.z, 2)):
			work_current_point.z = z
			delta_update()
			delta_write()
			time.sleep(0.1)

		for r in range(10, 150, 20):
			n = r*3
			for p in range(0, n+1):
				phi = 2*pi*p/n
				x = r*cos(phi)
				y = r*sin(phi)
				work_current_point.x = x
				work_current_point.y = y
				print(x, y)
				delta_update()
				delta_write()
				time.sleep(2/r)

	elif args[0] == "dots":

		def do_dot(h):
			home_z = int(work_current_point.z)
			for z in reversed(range(h, home_z+2, 2)):
				work_current_point.z = z
				delta_update()
				delta_write()
				time.sleep(0.2)
			for z in range(h, home_z+2, 2):
				work_current_point.z = z
				delta_update()
				delta_write()
				time.sleep(0.2)

		delta_update()
		delta_write()
		time.sleep(1)

		for z in reversed(range(30, work_current_point.z, 2)):
			work_current_point.z = z
			delta_update()
			delta_write()
			time.sleep(0.1)

		for x in range(-50, 60, 10):
			for y in range(-50, 60, 10):
				work_current_point.x = x
				work_current_point.y = y
				print(x, y)
				delta_update()
				delta_write()
				time.sleep(0.2)
				do_dot(int(15 - (x + 100)/20))



	print("Stop test")
else:

	delta_active = False


	font_size = 12
	pygame.init()
	# pygame.freetype.init()
	pygame.font.init()
	# font = pygame.freetype.SysFont("LiberationMono-Regular", font_size)
	# font = pygame.font.SysFont("LiberationMono-Regular", font_size)
	font = pygame.font.SysFont("DejaVuSansMono", font_size)

	BLACK = pygame.Color(0,0,0, 255)
	WHITE = pygame.Color(255, 255, 255, 255)
	GRAY = pygame.Color(150,150,150, 255)
	GREEN = pygame.Color(0, 255, 0, 255)
	RED = pygame.Color(255, 0, 0, 255)
	BLUE = pygame.Color(0, 0, 255, 255)

	window = (800, 600)
	W = pygame.display.set_mode(window)
	S = pygame.Surface(window, pygame.SRCALPHA)

	margin = 100
	field_R = int(window[1]/2) - margin

	graphics_delta_scale = field_R / work_R

	margin = int(window[1]/2) - field_R
	field_center = (window[0] - field_R - margin, int(window[1]/2))

	def graphics2work (pos):
		return (int((pos[0] - field_center[0]) / graphics_delta_scale), int((pos[1] - field_center[1]) / graphics_delta_scale))

	def work2graphics (pos):
		return (int(pos[0] * graphics_delta_scale) + field_center[0],
			int(pos[1] * graphics_delta_scale) + field_center[1])

	affector_graphics_pos = work2graphics((work_current_point.x, work_current_point.y))

	def render ():
		S.fill(GRAY)

		if delta_active:
			pygame.draw.circle(S, WHITE, field_center, field_R)
		else:
			pygame.draw.circle(S, BLACK, field_center, field_R)

		pygame.draw.rect(S, GREEN, (affector_graphics_pos[0]-10, affector_graphics_pos[1]-10, 20, 20))

		W.blit(S, (0, 0))

		text = []
		text.append("virtual workarea (mm):")
		text.append("x=%5d" % work_current_point.x)
		text.append("y=%5d" % work_current_point.y)
		text.append("z=%5d" % work_current_point.z)
		text.append("")
		text.append("delta workarea (mm):")
		text.append("x=%5d" % delta_current_point.x)
		text.append("y=%5d" % delta_current_point.y)
		text.append("z=%5d" % delta_current_point.z)
		text.append("")
		text.append("delta arm angles (degree):")
		text.append("a=%5d" % delta_current_angles[0])
		text.append("b=%5d" % delta_current_angles[1])
		text.append("c=%5d" % delta_current_angles[2])
		text.append("")
		text.append("pwm (us / 20ms):")
		text.append("servo #1: %5d" % delta_current_pwm[0])
		text.append("servo #1: %5d" % delta_current_pwm[1])
		text.append("servo #1: %5d" % delta_current_pwm[2])
		for idx, s in enumerate(text):
	#		label = font.render(s, fgcolor=BLACK)
			label = font.render(s, True, BLACK)
			W.blit(label, (10, 10 + idx*font_size))

		pygame.display.update()

	def update():
		global work_current_point
		global affector_graphics_pos

		delta_update()

		affector_graphics_pos = work2graphics((work_current_point.x, work_current_point.y))
		delta_write()

	running = True

	# move event -> new position -> count angles -> count pwm and write -> count back coordinates -> draw

	update()


	while running:
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				running = False

			if event.type == pygame.MOUSEMOTION:
				if delta_active:
					work_pos = graphics2work(event.pos)
					work_current_point.x = work_pos[0]
					work_current_point.y = work_pos[1]
					update()

			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if delta_active:
					work_current_point.z -= 10
					update()
					time.sleep(0.1)
					work_current_point.z += 10
					update()

			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
				if delta_active:
					delta_active = False
					delta_reset()
					affector_graphics_pos = work2graphics((work_current_point.x, work_current_point.y))
					delta_write()
				else:
					delta_active = True
					work_pos = graphics2work(event.pos)
					work_current_point.x = work_pos[0]
					work_current_point.y = work_pos[1]
					update()


			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
				# wheel up
				if delta_active:
					work_current_point.z -= 2
					update()

			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
				# wheel down
				if delta_active:
					work_current_point.z += 2
					update()
		render()









if opts["device_filename"]:
	port.close()
















