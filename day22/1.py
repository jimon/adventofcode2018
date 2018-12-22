
class Cave:
	def __init__(self, cave_depth, target_x, target_y):
		self.cave_depth = cave_depth
		self.target_x = target_x
		self.target_y = target_y
		self.w = target_x + 1
		self.h = target_y + 1

		self.erosion = [0 for y in range(0, self.h) for x in range(0, self.w)]
		for y in range(0, self.h):
			for x in range(0, self.w):
				if (x == 0 and y == 0) or (x == self.target_x and y == self.target_y):
					self.erosion[self.i((x, y))] = (0 + self.cave_depth) % 20183
				elif y == 0:
					self.erosion[self.i((x, y))] = (x * 16807 + self.cave_depth) % 20183
				elif x == 0:
					self.erosion[self.i((x, y))] = (y * 48271 + self.cave_depth) % 20183
				else:
					self.erosion[self.i((x, y))] = (self.erosion[self.i((x - 1, y))] * self.erosion[self.i((x, y - 1))] + self.cave_depth) % 20183

		self.m = [self.erosion[self.i((x, y))] % 3 for y in range(0, self.h) for x in range(0, self.w)]

	def i(self, key):
		x, y = key
		if x >= 0 and y >= 0 and x < self.w and y < self.h:
			return y * self.w + x
		else:
			return None

	def risk_level(self):
		return sum(self.m)

	def debug(self):
		d = ['.', '=', '|']
		print('----------------------')
		for y in range(0, self.h):
			print(''.join([d[x] for x in self.m[y*self.w:(y+1)*self.w]]))

c = Cave(9171, 7, 721)
#c.debug()
print(c.risk_level())

