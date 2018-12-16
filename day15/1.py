start_hp = 200
attack_dmg = 3

import scipy

m = [x.strip() for x in open('inputk.txt').readlines()]
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

def pathtocost(path):
	return sum([xytoi(x, y) for x, y in path])
def dijkstra_fill(m, f, x, y, cost, path):
	if x < 0 or y < 0 or x >= w or y >= h:
		return
	if not isfree(gettype(m, x, y)):
		return
	i = xytoi(x, y)
	if f[i][0] != -1 and f[i][0] < cost:
		return
	if f[i][0] == cost:
		if pathtocost(f[i][1]) <= pathtocost(path):
			return
	f[i] = (cost, path)
	for dx, dy in tlrb:
		dijkstra_fill(m, f, x + dx, y + dy, cost + 1, path + [(x + dx, y + dy)])
def dijkstra(m, x, y):
	f = [(-1, []) for i in range(0, w * h)]
	f[xytoi(x, y)] = (0, [])
	for dx, dy in tlrb:
		dijkstra_fill(m, f, x + dx, y + dy, 1, [(x + dx, y + dy)])
	return f
def dijkstra_cost(f, x, y):
	return (-1, []) if x < 0 or y < 0 or x >= w or y >= h else f[xytoi(x, y)]
def travelcost(f, x, y):
	a = [(*dijkstra_cost(f, x + dx, y + dy), xytoi(x + dx, y + dy)) for dx, dy in tlrb if dijkstra_cost(f, x + dx, y + dy)[0] >= 0]
	if len(a) == 0:
		return None
	b = sorted(a, key=lambda x:(x[0], x[2]))[0]
	assert(len(b) == 3)
	return b

def sim(m):
	units = [(m[i][0], m[i][1], i) for i in range(0, w * h) if ischaracter(m[i][0])]
	units = sorted(units, key=lambda k: k[2])

	for my_type, my_hp, my_i in units:
		x, y = itoxy(my_i)
		# dead
		if gettype(m, x, y) == '.':
			continue

		# TODO faster
		enemy_positions = {
			my_type: sorted([ (x, y) for y in range(0, h) for x in range(0, w) if gettype(m, x, y) == enemy_type],
			key=lambda k: xytoi(k[0], k[0])) for my_type, enemy_type in [('E', 'G'), ('G', 'E')]
		}

		if len(enemy_positions.get(my_type)) == 0:
			return False

		adj_enemy = [xytoi(x + dx, y + dy) for dx, dy in tlrb if isenemy(my_type, gettype(m, x + dx, y + dy))]
		adj_enemy = sorted(adj_enemy, key=lambda k:(m[k][1], k))

		if len(adj_enemy) > 0:
			ei = adj_enemy[0]
			et, eh = m[ei]
			eh -= attack_dmg
			if eh > 0:
				m[ei] = (et, eh)
				print(my_type, 'attacking ', et, 'at', *itoxy(ei))
			else:
				print(my_type, 'killing ', et, 'at', *itoxy(ei))
				m[ei] = ('.', -1)

		else:
			f = dijkstra(m, x, y)
			all_reachable = [travelcost(f, enemy_x, enemy_y) for enemy_x, enemy_y in enemy_positions.get(my_type)]
			all_reachable = [k for k in all_reachable if k is not None]
			all_reachable = sorted(all_reachable, key=lambda k: (k[0], k[2]))
			if len(all_reachable) == 0:
				continue
			
			to_x, to_y = all_reachable[0][1][0]

			#if my_type == 'E':
			#	deb([ (str(x if x <= 9 else 9) if x >= 0 else '.', 1) for x, path in f])
			#	print(all_reachable)
			m[my_i] = ('.', -1)
			m[xytoi(to_x, to_y)] = (my_type, my_hp)

			print('%s (%u,%u)->(%u,%u)' % (my_type, x, y, to_x, to_y))

	return True

def all_hp(m):
	return sum([m[i][1] for i in range(0, w * h) if m[i][0] in ['G', 'E']])

deb(m)

rounds = 0
while sim(m):
	rounds += 1
	deb(m)
	#print(rounds, all_hp(m), rounds * all_hp(m))
	#last_m = copy.copy(m)

	if rounds >= 29:
		break

#deb(m)

print(rounds, all_hp(m), rounds * all_hp(m))

#for i in range(0, 48):
	#sim(m)
	#deb(m)

for i in range(0, w * h):
	if m[i][0] in ['G', 'E']:
		print(m[i])