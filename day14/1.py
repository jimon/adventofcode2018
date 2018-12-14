d = [3, 7]
c0 = 0
c1 = 1

def sim(d, c0, c1):
    a = d[c0]
    b = d[c1]
    s = a + b

    if s >= 10:
        d.append(int(s / 10))
        d.append(s % 10)
    else:
        d.append(s)

    l = len(d)
    c0 = (c0 + a + 1) % l
    c1 = (c1 + b + 1) % l

    #print(''.join(['(%u)' % x if i == c0 else ('[%u]' % x if i == c1 else ' %u ' % x) for i, x in enumerate(d)]))
    return d, c0, c1

org_len = 260321
req_len = org_len + 10
while True:
    d, c0, c1 = sim(d, c0, c1)
    if len(d) >= req_len:
        break
print(''.join([str(x) for x in d[org_len:]]))

