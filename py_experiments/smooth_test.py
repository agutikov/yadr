#!/usr/bin/python

import sys
import io
from pprint import pprint
import math



def smooth (start, finish, step, v_max):

	def sign (x):
		return -1 if x < 0 else 1

	def break_path (v, step):
		s = 0
		count = 0
		while abs(v) > 0:
			if abs(v) <= abs(step):
				return s+v, count+1
			s += v
			v = (abs(v) - abs(step))*sign(v)
			count += 1
		return s, count

	result = []

	v = 0
	x = start
	bp = 0

# разгон и движение с постоянной скоростью пока до конца не останется тормозной путь плюс что-то до удвоенной величины скорости
	while abs(finish - x) > abs(bp + 2*v):
		if abs(v) < abs(v_max):
			v = v + step
			if abs(v) > abs(v_max):
				v = v_max
			bp += v
		if abs(finish - x) < abs(bp + 2*v):
			break
		x = x + v
		result.append(x)


# торможение с подстройкой скорости для плавного завершения движения в точке finish
# в то же время без превышения максимального ускорения
	while x != finish:
		bp, count = break_path(v, step)
		d = finish - x - bp
		j = int(d / count)
		if abs(j) > abs(step):
			j = step

		x = x + v
		result.append(x)

		if abs(v) > abs(step):
			v = v - step + j
			if abs(v) > abs(v_max):
				v = v_max
		elif abs(v) > abs(finish - x):
			v = finish - x

	return result


def smooth_test (start, finish, step, v_max):
	print("\nTest: ", start, finish, step, v_max)
	x = smooth(start, finish, step, v_max)
#	pprint(x)
	print("finish:", x[-1])
	if finish != x[-1]:
		print("Warning! Last value not correct!")

	x.insert(0, start)
	x.insert(0, start)
	x.append(finish)

	v = list(map(lambda a,b: abs(b-a), x, x[1:]))
#	pprint(v)
	print("max velocity:", max(v))
	if max(v) > abs(v_max):
		print("Warning! Maximum velocity exceeded!")

	a = list(map(lambda f,g: abs(g-f), v, v[1:]))
#	pprint(a)
	print("max acceleration:", max(a))
	if max(a) > abs(step):
		print("Warning! Maximum acceleration exceeded!")




smooth_test(100, 0, -3, -10)
smooth_test(100, -100, -10, -20)

smooth_test(0, 1000, 2, 100)
smooth_test(0, 10, 2, 100)
smooth_test(0, 10, 3, 5)





