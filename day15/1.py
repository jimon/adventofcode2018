start_hp = 5
attack_dmg = 3

import scipy

m = [x.strip() for x in open('inputk2.txt').readlines()]
w = len(m[0])
h = len(m)
m = [(k, start_hp) if k in ['G', 'E'] else (k, -1) for x in m for k in x]

def itoxy(i):
	return i % w, int(i / w)
def xytoi(x, y):
	return y * w + x
def gettype(m, x, y):
	if x < 0 or y < 0 or x >= w or y >= h:
		return None
	return m[xytoi(x, y)][0]
def isfree(your_type):
	return your_type == '.'
def ischaracter(your_type):
	return your_type in ['G', 'E']
def isenemy(your_type, enemy_type):
	return your_type in ['G', 'E'] and enemy_type in ['G', 'E'] and your_type != enemy_type
def deb(m):
	print('-----')
	for y in range(0, h):
		print(''.join([m[xytoi(x, y)][0] for x in range(0, w)]))


tlrb = [
	(0, -1),
	(-1, 0),
	( 1, 0),
	( 0, 1)
]

def dijkstra_fill(m, f, x, y, cost, path):
	if x < 0 or y < 0 or x >= w or y >= h:
		return
	if not isfree(gettype(m, x, y)):
		return
	i = xytoi(x, y)
	if f[i][0] != -1 and f[i][0] <= cost:
		return
	f[i] = (cost, path)
	for dx, dy in tlrb:
		dijkstra_fill(m, f, x + dx, y + dy, cost + 1, path + [(x + dx, y + dy)])
def dijkstra(m, x, y):
	f = [(-1, []) for i in range(0, w * h)]
	f[xytoi(x, y)] = (0, [])
	for dx, dy in tlrb:
		dijkstra_fill(m, f, x + dx, y + dy, 1, [(x + dx, y + dy)])
	#deb([ (str(x if x <= 9 else 9) if x >= 0 else '.', 1) for x, path in f])
	return f
def dijkstra_cost(f, x, y):
	return (-1, []) if x < 0 or y < 0 or x >= w or y >= h else f[xytoi(x, y)]
def travelcost(f, x, y):
	a = [(*dijkstra_cost(f, x + dx, y + dy), xytoi(x + dx, y + dy)) for dx, dy in tlrb if dijkstra_cost(f, x + dx, y + dy)[0] >= 0]
	if len(a) == 0:
		return None
	return sorted(a, key=lambda x:(x[0], x[2]))[0]

def sim(m):
	enemy_positions = {
		my_type: sorted(
			[ (x, y) for y in range(0, h) for x in range(0, w) if gettype(m, x, y) == enemy_type],
		key=lambda k: xytoi(k[0], k[0])) for my_type, enemy_type in [('E', 'G'), ('G', 'E')]
	}

	for y in range(0, h):
		for x in range(0, w):
			my_type = gettype(m, x, y)
			if not ischaracter(my_type):
				continue

			adj_enemy = [xytoi(x + dx, y + dy) for dx, dy in tlrb if isenemy(my_type, gettype(m, x + dx, y + dy))]

			# find where to move
			#if my_type != 'E':
			#	continue

			if len(adj_enemy) > 0:
				#ei = adj_enemy[0]
				#et, eh, em = m[ei]
				#eh -= attack_dmg
				#if eh > 0:
				#	m[ei] = (et, eh, em)
				#else:
				#	m[ei] = ('.', -1, False)
				pass
			else:

				f = dijkstra(m, x, y)

				all_reachable = [travelcost(f, enemy_x, enemy_y) for enemy_x, enemy_y in enemy_positions.get(my_type)]
				all_reachable = sorted(all_reachable, key=lambda x: (x[0], x[2]))

				if len(all_reachable) == 0:
					continue

				way_x, way_y = all_reachable[0][1][0]

				#mt, mh, mm = m[xytoi(x, y)]
				#m[xytoi(x, y)] = ('.', -1, False)
				#m[xytoi(way_x, way_y)] = (mt, mh, True)





deb(m)
for i in range(0, 15):
	sim(m)
	deb(m)

