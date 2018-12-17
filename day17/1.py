import re
#from collections import namedtuple

#Pos = namedtuple('Pos', 'x, y')

parse_line = re.compile(r"""([xy])=(\d+), ([xy])=(\d+)\.\.(\d+)""")

d = [parse_line.match(x.strip()).groups() for x in open('inputk.txt').readlines()]
d = [(x[0], int(x[1]), x[2], int(x[3]), int(x[4])) for x in d]
d = [((x[1], x[1]) if x[0] == 'x' else (x[3], x[4]), (x[3], x[4]) if x[0] == 'x' else (x[1], x[1])) for x in d]

x0 = min([x[0] for x, y in d])
y0 = min([y[0] for x, y in d])
d = [((x[0] - x0, x[1] - x0), (y[0] - y0, y[1] - y0)) for x, y in d]

w = max([x[1] for x, y in d])
h = max([y[1] for x, y in d])

print(d)
print(w,h)