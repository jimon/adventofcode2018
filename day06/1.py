import re

p = re.compile(r"""(\d+), (\d+)""")

def parse(x):
    k = p.match(x)
    if k is None:
        raise ValueError("invalid '%s'" % (x))
    g = k.groups()
    return (int(g[0]), int(g[1]))

d = [parse(x.strip()) for x in open("input1.txt").readlines()]
print(d)