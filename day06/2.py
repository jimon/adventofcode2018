import re

p = re.compile(r"""(\d+), (\d+)""")

def parse(i, x):
    k = p.match(x)
    if k is None:
        raise ValueError("invalid '%s'" % (x))
    g = k.groups()
    return (i, int(g[0]), int(g[1]))

d = [parse(i, x.strip()) for i, x in enumerate(open("input1.txt").readlines())]
#d = [(0, 1, 1), (1, 1, 6), (2, 8, 3), (3, 3, 4), (4, 5, 5), (5, 8, 9)]

min_x = min([x[1] for x in d])
max_x = max([x[1] for x in d])
min_y = min([x[2] for x in d])
max_y = max([x[2] for x in d])
if 0:
    d = [(x[0], x[1] - min_x, x[2] - min_y) for x in d]
    w = max_x - min_x
    h = max_y - min_y
else:
    w = max_x + 2
    h = max_y + 2

def dist(x0, y0, x1, y1):
    return abs(y1 - y0) + abs(x1 - x0)

def find_d(x, y, d):
    s = sum(dist(x, y, p[1], p[2]) for p in d)
    return s if s < 10000 else None

m = [ [ find_d(x, y, d) for y in range(0, h) ] for x in range(0, w)]

print(len([ 1 for x in range(0, w) for y in range(0, h) if m[x][y] is not None]))


# def index_to_str(x, y, d, m):
#     index = m[x][y]
#     k = [p[0] for p in d if p[1] == x and p[2] == y]
#     if index is None:
#         return '.'
#     elif len(k) > 0:
#         return chr(ord('A') + k[0] % 26)
#     else:
#         return '#'

# for y in range(0, h):
#     print(''.join([index_to_str(x, y, d, m) for x in range(0, w)]))

