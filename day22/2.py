
import networkx
from itertools import permutations

class Cave:
	def __init__(self, cave_depth, target_x, target_y):
		self.cave_depth = cave_depth
		self.target_x = target_x
		self.target_y = target_y
		self.w = target_x + 100
		self.h = target_y + 100

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

	def find_path(self):
		eq_none = 1
		eq_torch = 2
		eq_climbing = 4

		arround = [
			(-1,  0),
			( 0, -1),
			( 1,  0),
			( 0,  1),
		]

		allowed_types = {
			0: eq_torch + eq_climbing,
			1: eq_none + eq_climbing,
			2: eq_none + eq_torch,
		}

		am = [allowed_types[self.m[i]] for i in range(self.w * self.h)]

		def bits(number):
			bit = 1
			while number >= bit:
				if number & bit:
					yield bit
				bit <<= 1

		G = networkx.DiGraph()
		for y in range(0, self.h):
			for x in range(0, self.w):
				i = y * self.w + x
				for dx, dy in arround:
					x2 = x + dx
					y2 = y + dy
					if x2 < 0 or y2 < 0 or x2 >= self.w or y2 >= self.h:
						continue
					i2 = y2 * self.w + x2
					for at in bits(am[i] & am[i2]):
						G.add_edge((x, y, at), (x2, y2, at), weight=1)
				for at1, at2 in permutations(bits(am[i]), 2):
					G.add_edge((x, y, at1), (x, y, at2), weight=7)

		print(networkx.dijkstra_path_length(G, (0, 0, 2), (self.target_x, self.target_y, 2)))

	def debug(self):
		d = ['.', '=', '|']
		print('----------------------')
		for y in range(0, self.h):
			print(''.join([d[x] for x in self.m[y*self.w:(y+1)*self.w]]))


#c = Cave(510, 10, 10)
c = Cave(9171, 7, 721)
c.find_path()

# 986 is correct
