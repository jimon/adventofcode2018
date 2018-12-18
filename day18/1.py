
around_xy = [
	(-1,  1),
	( 0,  1),
	( 1,  1),
	(-1,  0),
	( 1,  0),
	(-1,  -1),
	( 0,  -1),
	( 1,  -1),
]

from collections import Counter

class Map:
	def __init__(self, filename):
		d = [x.strip() for x in open(filename).readlines()]
		self.w = len(d[0])
		self.h = len(d)
		self.m = [d[y][x] for y in range(0, self.h) for x in range(0, self.w)]

	def __getitem__(self, key):
		x, y = key
		if x < 0 or y < 0 or x >= self.w or y >= self.h:
			return None
		return self.m[y * self.w + x]

	def around(self, x, y):
		return Counter([self[x+dx,y+dy] for dx, dy in around_xy])

	def step(self, x, y):
		c = self[x, y]
		a = self.around(x, y)
		if c == '.' and a.get('|', 0) >= 3:
			return '|'
		elif c == '|' and a.get('#', 0) >= 3:
			return '#'
		elif c == '#':
			if a.get('#', 0) >= 1 and a.get('|', 0) >= 1:
				return '#'
			else:
				return '.'
		return c

	def sim(self):
		self.m = [self.step(x, y) for y in range(0, self.h) for x in range(0, self.w)]

	def value(self):
		c = Counter(self.m)
		return c.get('|', 0) * c.get('#', 0)

	def debug(self):
		print('----------------------')
		for y in range(0, self.h):
			print(''.join(self.m[y*self.w:(y+1)*self.w]))

m = Map('input1.txt')

for i in range(0, 10):
	m.sim()
print(m.value())

# d = []
# for i in range(0, 1000):
# 	if i % 100 == 0:
# 		print(i)
# 	m.sim()
# 	d.append(m.value())

# open('data.txt', 'wt').writelines(['%u\n' % x for x in d])
