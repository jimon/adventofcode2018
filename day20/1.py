
class Map:
	def __init__(self):
		self.org_x = 0
		self.org_y = 0
		self.w = 1
		self.h = 1
		self.m = ['?' for y in range(0, self.h) for x in range(0, self.w)]

	def __setitem__(self, key, value):
		x, y = key
		x += self.org_x
		y += self.org_y
		if x < 0:
			dx = -x
			self.org_x += dx
			wo = self.w
			self.w += dx
			self.m = [ self.m[y2 * wo + (x2 - dx)] if x2 >= dx else '?' for y2 in range(0, self.h) for x2 in range(0, self.w)]
			x = 0
		elif y < 0:
			dy = -y
			self.org_y += dy
			self.h += dy
			self.m = [ self.m[(y2 - dy) * self.w + x2] if y2 >= dy else '?' for y2 in range(0, self.h) for x2 in range(0, self.w)]
			y = 0
		elif x >= self.w:
			dx = self.w - x + 1
			wo = self.w
			self.w += dx
			self.m = [ self.m[y2 * wo + x2] if x2 < wo else '?' for y2 in range(0, self.h) for x2 in range(0, self.w)]
		elif y >= self.h:
			dy = self.h - y + 1
			ho = self.h
			self.h += dy
			self.m = [ self.m[y2 * self.w + x2] if y2 < ho else '?' for y2 in range(0, self.h) for x2 in range(0, self.w)]

		self.m[y * self.w + x] = value

	def __getitem__(self, key):
		x, y = key
		x += self.org_x
		y += self.org_y
		if x < 0 or y < 0 or x >= self.w or y >= self.h:
			return None
		return self.m[y * self.w + x]

	def debug(self):
		print('----------------------')
		print(''.join(['#' for i in range(0, self.w + 2)]))
		for y in range(0, self.h):
			print('#%s#' % (''.join(self.m[y*self.w:(y+1)*self.w])))
		print(''.join(['#' for i in range(0, self.w + 2)]))

	def freeze(self):
		self.m = ['#' if x == '?' else x for x in self.m]

	def setdot(self, l1, l2, count):
		if self[l1] == '?' or self[l1] == None or count < self[l1]:
			self[l1] = count
		self[l2] = '.'

	def move(self, c, d, count):
		if d == 'W':
			l1 = (c[0] - 1, c[1])
			l2 = (c[0] - 2, c[1])
			self.setdot(l1, l2, count)
			return l2
		elif d == 'E':
			l1 = (c[0] + 1, c[1])
			l2 = (c[0] + 2, c[1])
			self.setdot(l1, l2, count)
			return l2
		elif d == 'N':
			l1 = (c[0], c[1] - 1)
			l2 = (c[0], c[1] - 2)
			self.setdot(l1, l2, count)
			return l2
		elif d == 'S':
			l1 = (c[0], c[1] + 1)
			l2 = (c[0], c[1] + 2)
			self.setdot(l1, l2, count)
			return l2
		else:
			raise ValueError(d)

	def walk(self, c, i, d, count = 0):
		while i < len(d):
			if d[i] in ['W', 'N', 'E', 'S']:
				c = self.move(c, d[i], count)
				i += 1
				count += 1
			elif d[i] == '(':
				while d[i] != ')':
					c_ign, i = self.walk(c, i + 1, d, count)
				i += 1
			elif d[i] in [')', '|']:
				return (c, i)

		return (c, i)


m = Map()


d = open('input1.txt').readlines()[0].strip()[1:-1]

c = (0 ,0)
m[c] = 'X'

m.walk(c, 0, d)
m.freeze()

k = max([x for x in m.m if type(x) is int])
print(k + 1)

#m.debug()