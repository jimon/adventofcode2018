import re
#from collections import namedtuple

#Pos = namedtuple('Pos', 'x, y')

parse_line = re.compile(r"""([xy])=(\d+), ([xy])=(\d+)\.\.(\d+)""")

d = [parse_line.match(x.strip()).groups() for x in open('input1.txt').readlines()]
d = [(x[0], int(x[1]), x[2], int(x[3]), int(x[4])) for x in d]
d = [((x[1], x[1]) if x[0] == 'x' else (x[3], x[4]), (x[3], x[4]) if x[0] == 'x' else (x[1], x[1])) for x in d]

x0 = min([x[0] for x, y in d]) - 1
y0org = min([y[0] for x, y in d])
y0 = 0
d = [((x[0] - x0, x[1] - x0), (y[0] - y0, y[1] - y0)) for x, y in d]

w = max([x[1] for x, y in d]) + 1 + 1
h = max([y[1] for x, y in d]) + 1

def get(m, x, y):
    if x < 0 or y < 0 or x >= w or y >= h:
        return '.'
    return m[y][x]
def set(m, x, y, v):
    if x < 0 or y < 0 or x >= w or y >= h:
        return
    m[y][x] = v

m = [['.' for x in range(0, w)] for y in range(0, h)]
for xw, yh in d:
    for y in range(yh[0], yh[1] + 1):
        for x in range(xw[0], xw[1] + 1):
            set(m, x, y, '#')
set(m, 500 - x0, 0 - y0, '+')

def is_row_bound(m, x, y):
    xl = x
    xr = x
    while get(m, xl, y) == '~':
        xl -= 1
    while get(m, xr, y) == '~':
        xr += 1
    if get(m, xl, y) == '#' and get(m, xr, y) == '#':
        return True
    else:
        return False

def sim(m):
    for y in range(0, h):
        for x in range(0, w):
            if get(m, x, y) in ['+', '|']:
                if get(m, x, y + 1) == '.':
                    set(m, x, y + 1, '|')
                elif get(m, x, y + 1) in ['#', '~']:
                    xl = x - 1
                    xr = x + 1
                    while get(m, xl, y + 1) in ['#', '~'] and get(m, xl, y) in ['.', '|']:
                        xl -= 1
                    while get(m, xr, y + 1) in ['#', '~'] and get(m, xr, y) in ['.', '|']:
                        xr += 1
                    if get(m, xl, y) == '#' and get(m, xr, y) == '#':
                        for x2 in range(xl + 1, xr):
                            set(m, x2, y, '~')
                    else:
                        for x2 in range(xl + 1 - (1 if get(m, xl, y) != '#' else 0), xr + (1 if get(m, xr, y) != '#' else 0)):
                            set(m, x2, y, '|')

def deb(m, max_h = None):
    print('-----')
    for y in range(0, max_h if max_h is not None else h):
        print(''.join(m[y]))

#deb(m)
for i in range(0, 1000):
    if i % 100 == 0:
        print(i)
    sim(m)
deb(m)

total = len([1 for y in range(0, h) for x in range(0, w) if y >= y0org and get(m, x, y) in ['|', '~']])
total2 = len([1 for y in range(0, h) for x in range(0, w) if y >= y0org and get(m, x, y) == '~'])
print(total)
print(total2)

# 29068 is too high