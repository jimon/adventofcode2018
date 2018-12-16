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
		return readingordersort(units, self.w)

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

	def debug(self):
		print('-----')
		for y in range(0, self.h):
			print(''.join([str(self.get(x, y)) for x in range(0, self.w)]), ', '.join([ '%s: %u' % (self.get(x, y).t, self.get(x, y).h) for x in range(0, self.w) if self.get(x, y).isunit() ]))


class DistanceMap:
	class DistanceCell:
		def __init__(self, cost, came_from, w):
			self.cost = cost
			self.came_from = came_from
			self.w = w
		def visit(self, new_cost, came_from):
			if self.cost is not None and self.cost < new_cost:
				return False
			elif self.cost is None or self.cost > new_cost or (self.came_from.y * self.w + self.came_from.x) >= (came_from.y * self.w + came_from.x):
				self.cost = new_cost
				self.came_from = came_from
				return True
			else:
				return False

		def __str__(self):
			return str(self.cost if self.cost <= 9 else 9) if self.cost is not None else '.'

	def __init__(self, m, from_x, from_y, enemy_type):
		self.w = m.w
		self.h = m.h
		self.m = [[DistanceMap.DistanceCell(None, None, self.w) for x in range(0, self.w)] for y in range(0, self.h)]
		v = set([])
		h = []
		heappush(h, (0, Pos(x = from_x, y = from_y), None))
		while len(h):
			cost, pos, came_from = heappop(h)
			if self.get(pos.x, pos.y).visit(cost, came_from):
				v.add(pos)
				for dx, dy in tlrb:
					new_pos = Pos(x = pos.x + dx, y = pos.y + dy)
					if new_pos not in v:
						if m.get(new_pos.x, new_pos.y).isfree() or (enemy_type is not None and m.get(new_pos.x, new_pos.y).t == enemy_type):
							heappush(h, (cost + 1, new_pos, pos))
						else:
							v.add(pos)

	def get(self, x, y):
		if x < 0 or y < 0 or x >= self.w or y >= self.h:
			return DistanceMap.DistanceCell(None, None)
		return self.m[y][x]

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
			x, y = c.came_from
			c = self.get(x, y)
		return r[::-1]

	# def dijkstra(m, x, y):
	# 	f = [(-1, []) for i in range(0, w * h)]
	# 	f[xytoi(x, y)] = (0, [])
	# 	for dx, dy in tlrb:
	# 		dijkstra_fill(m, f, x + dx, y + dy, 1, [(x + dx, y + dy)])
	# 	return f

#def itoxy(i):
#	return i % w, int(i / w)
#def xytoi(x, y):
#	return y * w + x




def sim(m):
	for pos in m.units():
		if not m.isunitat(pos.x, pos.y):
			continue

		# attack adj enemies
		adjenemies = m.adjacentenemiesof(pos.x, pos.y)
		if len(adjenemies) > 0:
			m.attack(adjenemies[0].x, adjenemies[0].y)
			continue

		# list all enemies
		enemies = m.enemiesof(pos.x, pos.y)
		if len(enemies) == 0:
			break

		d = DistanceMap(m, pos.x, pos.y, m.get(pos.x, pos.y).getenemytype())
		enemies_cost = sorted([(d.costto(enemy_pos.x, enemy_pos.y), enemy_pos) for enemy_pos in enemies if d.costto(enemy_pos.x, enemy_pos.y) is not None], key=lambda x: x[0])
		enemies_cost = [x for x in enemies_cost if x[0] == enemies_cost[0][0]]
		enemies_cost = sorted(enemies_cost, key=lambda x: x[1].y * d.w + x[0])

		#print(enemies_cost)

		#d.debug()

		if len(enemies_cost) > 0:
			moving_to_enemy = enemies_cost[0][1]
			path = d.path(moving_to_enemy.x, moving_to_enemy.y)
			m.move(pos.x, pos.y, path[0].x, path[0].y)

m = Map('inputk.txt')
m.debug()
for i in range(0, 48):
	sim(m)
	m.debug()

# def sim(m):
# 	units = [(m[i][0], m[i][1], i) for i in range(0, w * h) if ischaracter(m[i][0])]
# 	units = sorted(units, key=lambda k: k[2])

# 	for my_type, my_hp, my_i in units:
# 		x, y = itoxy(my_i)
# 		# dead
# 		if gettype(m, x, y) == '.':
# 			continue

# 		# TODO faster
# 		enemy_positions = {
# 			my_type: sorted([ (x, y) for y in range(0, h) for x in range(0, w) if gettype(m, x, y) == enemy_type],
# 			key=lambda k: xytoi(k[0], k[0])) for my_type, enemy_type in [('E', 'G'), ('G', 'E')]
# 		}

# 		if len(enemy_positions.get(my_type)) == 0:
# 			return False

# 		adj_enemy = [xytoi(x + dx, y + dy) for dx, dy in tlrb if isenemy(my_type, gettype(m, x + dx, y + dy))]
# 		adj_enemy = sorted(adj_enemy, key=lambda k:(m[k][1], k))

# 		if len(adj_enemy) > 0:
# 			ei = adj_enemy[0]
# 			et, eh = m[ei]
# 			eh -= attack_dmg
# 			if eh > 0:
# 				m[ei] = (et, eh)
# 				print(my_type, 'attacking ', et, 'at', *itoxy(ei))
# 			else:
# 				print(my_type, 'killing ', et, 'at', *itoxy(ei))
# 				m[ei] = ('.', -1)

# 		else:
# 			f = dijkstra(m, x, y)
# 			all_reachable = [travelcost(f, enemy_x, enemy_y) for enemy_x, enemy_y in enemy_positions.get(my_type)]
# 			all_reachable = [k for k in all_reachable if k is not None]
# 			all_reachable = sorted(all_reachable, key=lambda k: (k[0], k[2]))
# 			if len(all_reachable) == 0:
# 				continue
			
# 			to_x, to_y = all_reachable[0][1][0]

# 			#if my_type == 'E':
# 			#	deb([ (str(x if x <= 9 else 9) if x >= 0 else '.', 1) for x, path in f])
# 			#	print(all_reachable)
# 			m[my_i] = ('.', -1)
# 			m[xytoi(to_x, to_y)] = (my_type, my_hp)

# 			print('%s (%u,%u)->(%u,%u)' % (my_type, x, y, to_x, to_y))

# 	return True

# def all_hp(m):
# 	return sum([m[i][1] for i in range(0, w * h) if m[i][0] in ['G', 'E']])

# deb(m)

# rounds = 0
# while sim(m):
# 	rounds += 1
# 	deb(m)
# 	#print(rounds, all_hp(m), rounds * all_hp(m))
# 	#last_m = copy.copy(m)

# 	if rounds >= 29:
# 		break

#deb(m)

# print(rounds, all_hp(m), rounds * all_hp(m))

#for i in range(0, 48):
	#sim(m)
	#deb(m)

# for i in range(0, w * h):
# 	if m[i][0] in ['G', 'E']:
# 		print(m[i])