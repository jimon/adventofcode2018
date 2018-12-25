import re

def parse(filename):
	m = re.compile(r"""^\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*$""")
	d = [[int(y) for y in m.match(x.strip()).groups()] for x in open(filename).readlines() if len(x.strip()) > 0]
	d = [(x[0], x[1], x[2], x[3]) for x in d]
	for i, p0 in enumerate(d):
		for j, p1 in enumerate(d):
			if i != j:
				assert p0 != p1
	return d

def dist(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2]) + abs(a[3] - b[3])

def solve(d):
	constellations = []

	for p0 in d:
		add_to = []

		for i, constellation in enumerate(constellations):
			for p1 in constellation:
				if dist(p0, p1) <= 3:
					add_to.append(i)
					break

		# all unique
		#assert len(add_to) == len(list(set(add_to)))

		if len(add_to) > 0:
			u = [j for i in add_to for j in constellations[i]] + [p0]
			constellations = [constellation for i, constellation in enumerate(constellations) if i not in add_to] + [u]
		else:
			constellations.append([p0])

	#for constellation in constellations:
	#	if len(constellation) > 1:
	#		for i, p0 in enumerate(constellation):
	#			assert all([p0 != p1 for j, p1 in enumerate(constellation) if i != j])
	#			assert any([dist(p0, p1) <= 3 for j, p1 in enumerate(constellation) if i != j])

	return len(constellations)

print(solve(parse('inputk.txt')) == 2)
print(solve(parse('inputk2.txt')) == 4)
print(solve(parse('inputk3.txt')) == 3)
print(solve(parse('inputk4.txt')) == 8)

print(solve(parse('input1.txt'))) # 390
