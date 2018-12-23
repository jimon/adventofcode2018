import re

def parse(filename):
	rex = re.compile(r"""pos=<(-?\d+),(-?\d+),(-?\d+)>,\s*r=(-?\d+)""")
	return [[int(y) for y in rex.match(x.strip()).groups()] for x in open(filename).readlines()]

d = parse('input1.txt')

def find_with_dist(x0, y0, z0, x1, y1, z1, dist, d):
	max_in_range = 0
	max_in_range_dist_to_zero = None
	max_in_range_point = None

	for x in range(x0, x1 + 1, dist):
		for y in range(y0, y1 + 1, dist):
			for z in range(z0, z1 + 1, dist):

				in_range = 0
				for bx, by, bz, bd in d:
					k = abs(x - bx) + abs(y - by) + abs(z - bz)
					if k - bd + 1 <= dist:
						in_range += 1
				if in_range == 0:
					continue

				dist_to_zero = abs(x) + abs(y) + abs(z)

				if (in_range > max_in_range) or (in_range == max_in_range and dist_to_zero < max_in_range_dist_to_zero):
					max_in_range = in_range
					max_in_range_dist_to_zero = dist_to_zero
					max_in_range_point = (x, y, z)

	return max_in_range_point

x0 = min([p[0] for p in d])
y0 = min([p[1] for p in d])
z0 = min([p[2] for p in d])
x1 = max([p[0] for p in d])
y1 = max([p[1] for p in d])
z1 = max([p[2] for p in d])

def next_power_of_2(x):
	return 1 if x == 0 else 2**(x - 1).bit_length()
dist = next_power_of_2(max([x1 - x0, y1 - y0, z1 - z0]))

bx = int((x1 - x0) / 2)
by = int((y1 - y0) / 2)
bz = int((z1 - z0) / 2)
x0 = bx - dist
x1 = bx + dist
y0 = by - dist
y1 = by + dist
z0 = bz - dist
z1 = bz + dist

while dist > 0:
	print('------', dist)
	bx, by, bz = find_with_dist(x0, y0, z0, x1, y1, z1, dist, d)
	print(bx, by, bz, abs(bx) + abs(by) + abs(bz))
	x0 = bx - dist
	x1 = bx + dist
	y0 = by - dist
	y1 = by + dist
	z0 = bz - dist
	z1 = bz + dist
	dist = int(dist / 2)


# 101599540