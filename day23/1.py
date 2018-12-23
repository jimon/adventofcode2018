import re

def parse(filename):
	rex = re.compile(r"""pos=<(-?\d+),(-?\d+),(-?\d+)>,\s*r=(-?\d+)""")
	return [[int(y) for y in rex.match(x.strip()).groups()] for x in open(filename).readlines()]

d = parse('input1.txt')

largest_radius = max([k[3] for k in d])
largest = [b for b in d if b[3] == largest_radius]
assert(len(largest) == 1)
largest = largest[0]

def dist(p0, p1):
	return sum([abs(p0[i] - p1[i]) for i in range(0, 3)])

in_radius = [b for b in d if dist(b, largest) <= largest_radius]

print(len(in_radius))