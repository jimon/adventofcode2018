start_hp = 200
attack_dmg = 3

import scipy

m = [x.strip() for x in open('inputk2.txt').readlines()]
w = len(m[0])
h = len(m)
m = [(k, start_hp) if k in ['G', 'E'] else (k, 0) for x in m for k in x]

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


def dijkstra_fill(m, f, x, y, cost):
	if x < 0 or y < 0 or x >= w or y >= h:
		return
	if not isfree(gettype(m, x, y)):
		return
	i = xytoi(x, y)
	if f[i] != -1 and f[i] <= cost:
		return
	f[i] = cost
	dijkstra_fill(m, f, x - 1, y, cost + 1)
	dijkstra_fill(m, f, x + 1, y, cost + 1)
	dijkstra_fill(m, f, x, y - 1, cost + 1)
	dijkstra_fill(m, f, x, y + 1, cost + 1)
def dijkstra(m, from_x, from_y, to_x, to_y):
	f = [-1 for i in range(0, w * h)]
	dijkstra_fill(m, f, from_x, from_y, 0)
	deb([ (str(x) if x >= 0 else '.', 1) for x in f])

def sim(m):
	m2 = m

	for y in range(0, h):
		for x in range(0, w):
			my_type = gettype(m, x, y)
			if not ischaracter(my_type):
				continue

			enemy_t = isenemy(my_type, gettype(m, x, y - 1))
			enemy_l = isenemy(my_type, gettype(m, x - 1, y))
			enemy_r = isenemy(my_type, gettype(m, x + 1, y))
			enemy_b = isenemy(my_type, gettype(m, x, y + 1))

			if enemy_t or enemy_l or enemy_r or enemy_b:
				# attach
				pass
			else:
				# find where to move

				#scipy.sparse.csgraph.shortest_path()

				pass


	return m2


deb(m)

dijkstra(m, 2, 2, 4, 4)
#m = sim(m)
#deb(m)