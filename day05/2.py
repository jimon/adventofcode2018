d = [x.strip() for x in open("input1.txt").readlines()]
d = list(d[0])

def match(x, y):
    if x is None or y is None:
        return False
    x = (x.lower(), x)
    y = (y.lower(), y)
    return (x[0] == y[0]) and (x[1] != y[1])

def solve(d):
    work = True
    while work:
        work = False
        for i in range(0, len(d) - 1):
            if match(d[i], d[i + 1]):
                d[i] = None
                d[i + 1] = None
                work = True
        d = [x for x in d if x is not None]
    return len(d)

def drop(d, l):
    l = l.lower()
    for i in range(0, len(d)):
        if d[i] is not None and d[i].lower() == l:
            d[i] = None
    return [x for x in d if x is not None]

#d = ['a', 'A', 'b', 'B', 'C', 'D', 'C']

s = sorted([(x, solve(drop(d, x))) for x in list('abcdefghijklmnopqrstuvwxyz')], key = lambda x: x[1], reverse = True)
print(s)


