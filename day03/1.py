import re

d = [x.strip() for x in open("input1.txt").readlines()]
d = [[int(x) for x in re.split("@|:|,|x", sq[1:])] for sq in d]

w = max([ x[1] + x[3] for x in d ] )
h = max([ x[2] + x[4] for x in d ] )

# print(d[0])
print(w, h)
# print(d)

field = [[0 for y in range(0, h)] for x in range(0, w)]
#print(field)

for sq in d:
    for x in range(sq[1], sq[1] + sq[3]):
        for y in range(sq[2], sq[2] + sq[4]):
            field[x][y] += 1;

r = sum([1 for x in range(0, w) for y in range(0, h) if field[x][y] > 1])
print(r)