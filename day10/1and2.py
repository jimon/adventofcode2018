import re

p = re.compile(r"""position=<\s*([-\d]+),\s*([-\d]+)> velocity=<\s*([-\d]+),\s*([-\d]+)>""")

def parse(x):
	k = p.match(x)
	if k is None:
		raise ValueError("invalid string " + x)
	k = k.groups()
	return (int(k[0]), int(k[1]), int(k[2]), int(k[3]))

d = [parse(x) for x in open("input1.txt").readlines()]

def sim(d):
	return [(x[0] + x[2], x[1] + x[3], x[2], x[3]) for x in d]

def rectsq(d):
	x0 = min([x[0] for x in d])
	x1 = max([x[0] for x in d])
	y0 = min([x[1] for x in d])
	y1 = max([x[1] for x in d])
	return x1 - x0 + 1 + y1 - y0 + 1

def mapprint(d):
	x0 = min([x[0] for x in d])
	x1 = max([x[0] for x in d])
	y0 = min([x[1] for x in d])
	y1 = max([x[1] for x in d])
	points = set([(x[0], x[1]) for x in d])

	for y in range(y0, y1 + 1):
		print(''.join(['#' if (x, y) in points else '.' for x in range(x0, x1 + 1)]))

k = rectsq(d)
i = 0
while True:
	d2 = d
	d = sim(d)
	k2 = rectsq(d)
	if k2 >= k:
		mapprint(d2)
		print('sec:', i)
		break
	else:
		i += 1
		k = k2