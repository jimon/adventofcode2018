idata = [x.rstrip('\n') for x in open('input1.txt').readlines()]
w = len(idata[0])
h = len(idata)
idata = [x[:w] for x in idata]

def getxy(grid, x, y):
	if x < 0 or y < 0 or x >= w or y >= h:
		return None
	return grid[y][x]

def getxy33(grid, x, y):
	if x < 0 or y < 0 or x >= 3 or y >= 3:
		return None
	return grid[y][x]

def itoxy(i):
	return i % w, int(i / w)
def xytoi(x, y):
	return y * w + x

char_hor = ['-', '+', '>', '<']
char_vrt = ['|', '+', 'v', '^']
char_crt = ['>', '<', 'v', '^']

# this
# /---\
# |   |
# |   |
# \---/
#
# becomes
# 1---2
# |   |
# |   |
# 3---4

def input_to_map(grid, x, y):
	cell33 = [[getxy(grid, x + dx, y + dy) for dx in range(-1, 2)] for dy in range(-1, 2)]
	cell = getxy33(cell33, 1, 1)
	if cell == '/':
		if getxy33(cell33, 2, 1) in char_hor and getxy33(cell33, 1, 2) in char_vrt:
			return '1'
		elif getxy33(cell33, 0, 1) in char_hor and getxy33(cell33, 1, 0) in char_vrt:
			return '4'
		else:
			assert(None)
	elif cell == '\\':
		if getxy33(cell33, 0, 1) in char_hor and getxy33(cell33, 1, 2) in char_vrt:
			return '2'
		elif getxy33(cell33, 2, 1) in char_hor and getxy33(cell33, 1, 0) in char_vrt:
			return '3'
		else:
			assert(None)
	elif cell == '>' or cell == '<':
		return '-'
	elif cell == 'v' or cell == '^':
		return '|'
	else:
		return cell

# map grid
m = [input_to_map(idata, *itoxy(k)) for k in range(0, w * h)]

# carts
carts = []
for y in range(0, h):
	for x in range(0, w):
		cell = getxy(idata, x, y)
		if cell in char_crt:
			carts.append((x, y, cell, '<'))

def nextcoord(x1, y1, d):
	if d == '<':
		return x1 - 1, y1
	elif d == '^':
		return x1, y1 - 1
	elif d == '>':
		return x1 + 1, y1
	elif d == 'v':
		return x1, y1 + 1
	else:
		assert(False)

def dirrot90(d):
	if d == '<':
		return '^'
	elif d == '^':
		return '>'
	elif d == '>':
		return 'v'
	elif d == 'v':
		return '<'

def dirrot270(d):
	if d == '<':
		return 'v'
	elif d == '^':
		return '<'
	elif d == '>':
		return '^'
	elif d == 'v':
		return '>'

def sim(carts, m):
	carts = sorted(carts, key = lambda x: xytoi(x[0], x[1]))
	carts2 = []

	for index, cart in enumerate(carts):
		x = cart[0]
		y = cart[1]
		d = cart[2]
		e = cart[3]

		x, y = nextcoord(x, y, d)
		c = m[xytoi(x, y)]
		if c == '+':
			if e == '<':
				d = dirrot270(d)
			elif e == '^':
				pass
			elif e == '>':
				d = dirrot90(d)

			if e == '<':
				e = '^'
			elif e == '^':
				e = '>'
			elif e == '>':
				e = '<'
		elif d == '>':
			if c == '-':
				d = '>'
			elif c == '2':
				d = 'v'
			elif c == '4':
				d = '^'
			else:
				assert(False)
		elif d == '<':
			if c == '-':
				d = '<'
			elif c == '1':
				d = 'v'
			elif c == '3':
				d = '^'
			else:
				assert(False)
		elif d == '^':
			if c == '|':
				d = '^'
			elif c == '1':
				d = '>'
			elif c == '2':
				d = '<'
			else:
				assert(False)
		elif d == 'v':
			if c == '|':
				d = 'v'
			elif c == '3':
				d = '>'
			elif c == '4':
				d = '<'
			else:
				assert(False)
		carts2.append((x, y, d, e))

		seen = set([])
		for cart in carts[index+1:] + carts2:
			p = (cart[0], cart[1])
			if p in seen:
				print('collision at %u,%u' % (p[0], p[1]))
				exit(0)
			else:
				seen.add(p)


	return carts2


def deb(i, carts, m):
	print('----- iteration %03u' % i)
	carts_dict = { (x, y): d for x, y, d, e in carts }
	#print(carts_dict)
	for y in range(0, h):
		print(''.join([carts_dict.get((x, y), str(k)) for x, k in enumerate(m[xytoi(0, y):xytoi(0, y + 1)])]))

while True:
	carts = sim(carts, m)
