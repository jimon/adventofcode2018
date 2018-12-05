d = [x.strip() for x in open("input1.txt").readlines()]

def match(x, y):
    x = (x.lower(), x.isupper())
    y = (y.lower(), y.isupper())
    return (x[0] == y[0]) and (x[1] != y[1])

d = list(d[0])

work = True
#c = 0
while work:
    work = False
    for i in range(0, len(d) - 1):
        if match(d[i], d[i + 1]):
            d = d[:i] + d[i + 2:]
            work = True
            break
    #c += 1
    #print(c)

print(len(d))