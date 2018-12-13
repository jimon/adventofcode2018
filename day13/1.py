idata = [x.rstrip('\n') for x in open('inputk.txt').readlines()]
width = len(idata[0])
height = len(idata)
idata = [x[:width] for x in idata]

# transform every map cell into 3x3 segments
# this way there is no need to handle special cases like ||
input_to_map_dict = {
	'/t': [
		0, 0, 0,
		0, 1, 1,
		0, 1, 0
	],
	'\\t': [
		0, 0, 0,
		1, 1, 0,
		0, 1, 0
	],
	'/b': [
		0, 1, 0,
		1, 1, 0,
		0, 0, 0
	],
	'\\b': [
		0, 1, 0,
		0, 1, 1,
		0, 0, 0
	],
	'-': [
		0, 0, 0,
		1, 1, 1,
		0, 0, 0
	],
	'>': [
		0, 0, 0,
		1, 1, 1,
		0, 0, 0
	],
	'<': [
		0, 0, 0,
		1, 1, 1,
		0, 0, 0
	],
	'|': [
		0, 1, 0,
		0, 1, 0,
		0, 1, 0
	],
	'v': [
		0, 1, 0,
		0, 1, 0,
		0, 1, 0
	],
	'^': [
		0, 1, 0,
		0, 1, 0,
		0, 1, 0
	],
	'+': [
		0, 1, 0,
		1, 2, 1,
		0, 1, 0
	],
	' ': [
		0, 0, 0,
		0, 0, 0,
		0, 0, 0,
	]
}

input_to_cart_dict = {
	'<': 'l',
	'^': 't',
	'>': 'r',
	'v': 'b'
}

def getxy(grid, x, y, w, h):
	if x < 0 or y < 0 or x >= w or y >= h:
		return None
	return grid[y][x]

def getxy33(grid, x, y):
	return getxy(grid, x, y, 3, 3)

char_hor = ['-', '+', '>', '<']
char_vrt = ['|', '+', 'v', '^']
char_crt = ['>', '<', 'v', '^']

def input_to_map(grid, x, y, w, h):
	cell33 = [[getxy(grid, x + dx, y + dy, w, h) for dx in range(-1, 2)] for dy in range(-1, 2)]
	cell = getxy33(cell33, 1, 1)
	if cell == '/':
		if getxy33(cell33, 2, 1) in char_hor and getxy33(cell33, 1, 2) in char_vrt:
			cell = '/t'
		elif getxy33(cell33, 0, 1) in char_hor and getxy33(cell33, 1, 0) in char_vrt:
			cell = '/b'
		else:
			assert(None)
	elif cell == '\\':
		if getxy33(cell33, 0, 1) in char_hor and getxy33(cell33, 1, 2) in char_vrt:
			cell = '\\t'
		elif getxy33(cell33, 2, 1) in char_hor and getxy33(cell33, 1, 0) in char_vrt:
			cell = '\\b'
		else:
			assert(None)
	#assert(cell in input_to_map_dict)
	if cell not in input_to_map_dict:
		raise ValueError('unknown %s' % cell33)
	return input_to_map_dict.get(cell)

# map grid
mgw = width * 3
mgh = height * 3
mg = [0 for k in range(0, mgw * mgh)]

for y0 in range(0, height):
	for x0 in range(0, width):
		grid33 = input_to_map(idata, x0, y0, width, height)
		for y1 in range(0, 3):
			for x1 in range(0, 3):
				mg[(y0 * 3 + y1) * mgw + (x0 * 3 + x1)] = grid33[y1 * 3 + x1]

# carts
carts = []
for y0 in range(0, height):
	for x0 in range(0, width):
		cell = getxy(idata, x0, y0, width, height)
		if cell in char_crt:
			carts.append((x0, y0, input_to_cart_dict.get(cell)))

carts_dict = { (x * 3 + 1, y * 3 + 1): d for x, y, d in carts }

for y1 in range(0, mgh):
	print(''.join([carts_dict.get((x1, y1), str(k)) for x1, k in enumerate(mg[y1*mgw:y1*mgw+mgw])]))