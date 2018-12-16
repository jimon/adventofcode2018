from heapq import *
from collections import namedtuple

start_hp = 200
attack_dmg = 3

tlrb = [
	(0, -1),
	(-1, 0),
	( 1, 0),
	( 0, 1)
]

Pos = namedtuple('Pos', 'x, y')

def readingordersort(l, w):
	return sorted(l, key=lambda k: k.y * w + k.x)

class Map:
	class Cell:
		def __init__(self, unit_type):
			self.t = unit_type
			self.h = start_hp
		def isunit(self):
			return self.t in ['G', 'E']
		def getenemytype(self):
			return 'E' if self.t == 'G' else 'G'
		def isfree(self):
			return self.t == '.'
		def __str__(self):
			return self.t

	def __init__(self, filename):
		m = [x.strip() for x in open(filename).readlines()]
		self.w = len(m[0])
		self.h = len(m)
		self.m = [[Map.Cell(m[y][x]) for x in range(0, self.w)] for y in range(0, self.h)]

	def get(self, x, y):
		if x < 0 or y < 0 or x >= self.w or y >= self.h:
			return Cell('#')
		return self.m[y][x]

	def size(self):
		return self.w * self.h

	def units(self):
		units = [Pos(x=x, y=y) for y in range(0, self.h) for x in range(0, self.w) if self.get(x, y).isunit()]
		return readingordersort(units, self.w)

	def enemiesof(self, x, y):
		t = self.get(x, y).getenemytype()
		units = [Pos(x=x, y=y) for y in range(0, self.h) for x in range(0, self.w) if self.get(x, y).t == t]
		return readingordersort(units, self.w)

	def adjacentenemiesof(self, x, y):
		t = self.get(x, y).getenemytype()
		units = [Pos(x=x+dx,y=y+dy) for dx, dy in tlrb if self.get(x + dx, y + dy).t == t]
		return sorted(units, key=lambda pos: self.get(pos.x, pos.y).h)

	def isunitat(self, x, y):
		return self.get(x, y).isunit()

	def attack(self, x, y):
		self.get(x, y).h -= attack_dmg
		if self.get(x, y).h <= 0:
			self.get(x, y).t = '.'

	def move(self, from_x, from_y, to_x, to_y):
		assert(self.get(to_x, to_y).t == '.')
		self.m[to_y][to_x] = self.get(from_x, from_y)
		self.m[from_y][from_x] = Map.Cell('.')

	def tryattack(self, x, y):
		adjenemies = self.adjacentenemiesof(x, y)
		if len(adjenemies) > 0:
			self.attack(adjenemies[0].x, adjenemies[0].y)
			return True
		return False

	def allhp(self):
		return sum([self.get(pos.x,pos.y).h for pos in self.units()])

	def debug(self):
		print('-----')
		for y in range(0, self.h):
			print(''.join([str(self.get(x, y)) for x in range(0, self.w)]), ', '.join([ '%s: %u' % (self.get(x, y).t, self.get(x, y).h) for x in range(0, self.w) if self.get(x, y).isunit() ]))


class DistanceMap:
	class DistanceCell:
		def __init__(self, w):
			self.cost = None
			self.came_from_x = None
			self.came_from_y = None
			self.w = w
		def visit(self, new_cost, came_from_x, came_from_y):
			if self.cost is not None and self.cost < new_cost:
				return False
			elif self.cost is None or self.cost > new_cost or (self.came_from_y * self.w + self.came_from_x) >= (came_from_y * self.w + came_from_x):
				self.cost = new_cost
				self.came_from_x = came_from_x
				self.came_from_y = came_from_y
				return True
			else:
				return False

		def __str__(self):
			return str(self.cost if self.cost <= 9 else 9) if self.cost is not None else '.'

	def __init__(self, m, from_x, from_y, enemy_type):
		self.m = m
		self.w = m.w
		self.h = m.h
		self.enemy_type = enemy_type
		self.m2 = [[DistanceMap.DistanceCell(self.w) for x in range(0, self.w)] for y in range(0, self.h)]
		self.fill(0, from_x, from_y, None, None)

	def fill(self, cost, x, y, came_from_x, came_from_y):
		if not self.get(x, y).visit(cost, came_from_x, came_from_y):
			return
		for dx, dy in tlrb:
			nx = x + dx
			ny = y + dy
			if self.m.get(nx, ny).isfree() or m.get(nx, ny).t == self.enemy_type:
				self.fill(cost + 1, nx, ny, x, y)

	def get(self, x, y):
		if x < 0 or y < 0 or x >= self.w or y >= self.h:
			return DistanceMap.DistanceCell(None, None)
		return self.m2[y][x]

	def debug(self):
		print('-----')
		for y in range(0, self.h):
			print(''.join([str(self.get(x, y)) for x in range(0, self.w)]))

	def costto(self, x, y):
		return self.get(x, y).cost

	def path(self, x, y):
		c = self.get(x, y)
		r = []
		while c.cost is not None and c.cost > 0:
			r.append(Pos(x=x, y=y))
			x, y = c.came_from_x, c.came_from_y
			c = self.get(x, y)
		return r[::-1]

def sim(m):
	units = m.units()
	for i, pos in enumerate(units):
		print('%02u/%02u' % (i, len(units) - 1))
		if not m.isunitat(pos.x, pos.y):
			continue

		# attack adj enemies
		if m.tryattack(pos.x, pos.y):
			continue

		# list all enemies
		enemies = m.enemiesof(pos.x, pos.y)
		if len(enemies) == 0:
			return False

		d = DistanceMap(m, pos.x, pos.y, m.get(pos.x, pos.y).getenemytype())
		enemies_cost = sorted([(d.costto(enemy_pos.x, enemy_pos.y), enemy_pos) for enemy_pos in enemies if d.costto(enemy_pos.x, enemy_pos.y) is not None], key=lambda x: x[0])
		enemies_cost = [x for x in enemies_cost if x[0] == enemies_cost[0][0]]
		enemies_cost = sorted(enemies_cost, key=lambda x: x[1].y * d.w + x[0])

		if len(enemies_cost) > 0:
			moving_to_enemy = enemies_cost[0][1]
			path = d.path(moving_to_enemy.x, moving_to_enemy.y)
			new_pos = path[0]
			m.move(pos.x, pos.y, new_pos.x, new_pos.y)
			m.tryattack(new_pos.x, new_pos.y)

	return True

m = Map('input1.txt')
rounds = 0
while sim(m):
	rounds += 1
	print('------ round', rounds)

print(rounds * m.allhp())
