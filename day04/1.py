import re

p = re.compile(r"""\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (Guard #(\d+) begins shift|falls asleep|wakes up)""")


def parse(x):
    k = p.match(x)
    if k is None:
        raise ValueError("invalid '%s'" % (x))
    g = k.groups()
    return (int(g[0]),
            int(g[1]),
            int(g[2]),
            int(g[3]),
            int(g[4]),
            (0 if g[5][0] == 'G' else (1 if g[5][0] == 'f' else 2)),
            int(g[6]) if g[5][0] == 'G' else 0
   )

d = [parse(x.strip()) for x in open("input1.txt").readlines()]

begin_year = min([x[0] for x in d])

def date_to_minutes(year, month, day, hour, minute):
    days = (year - begin_year) * 366 + month * 31 + day
    return days * 24 * 60 + hour * 60 + minute
def date_to_minutes_x(x):
    return date_to_minutes(x[0], x[1], x[2], x[3], x[4])

d = [(date_to_minutes_x(x), (date_to_minutes_x(x) % 24*60), x[6], x[5], x[4]) for x in d]
d = sorted(d, key = lambda x: x[0])

# - timestamp
# - timestamp with-in 24h
# - id
# - 0 begins, 1 falls, 2 wakes
# - event minute

print(d[::10])


