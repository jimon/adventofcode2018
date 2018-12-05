d = [x.strip() for x in open("input1.txt").readlines()]

def match(x, y):
    if x is None or y is None:
        return False
    x = (x.lower(), x)
    y = (y.lower(), y)
    return (x[0] == y[0]) and (x[1] != y[1])

d = list(d[0])

work = True
c = 0
while work:
    work = False
    for i in range(0, len(d) - 1):
        if match(d[i], d[i + 1]):
            d[i] = None
            d[i + 1] = None
            work = True

    d = [x for x in d if x is not None]
    c += 1
    print(c)

    #print(d)

print(len(d))