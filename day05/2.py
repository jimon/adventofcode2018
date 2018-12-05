org_d = [x.strip() for x in open("input1.txt").readlines()]
org_d = list(org_d[0])

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


#org_d = ['a', 'A', 'b', 'B', 'C', 'D', 'C']

s = [(x, solve([y for y in org_d if y.lower() != x.lower()])) for x in list('abcdefghijklmnopqrstuvwxyz')]
s = sorted(s, key = lambda x: x[1])
print(s)


