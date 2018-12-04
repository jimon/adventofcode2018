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
    if hour > 0:
        day += 1
        hour = 0
        minute = 0
    days = (year - begin_year) * 366 + month * 31 + day
    return days * 24 * 60 + hour * 60 + minute
def date_to_minutes_x(x):
    return date_to_minutes(x[0], x[1], x[2], x[3], x[4])

d = [(date_to_minutes_x(x), (date_to_minutes_x(x) % (24*60)), x[6], x[5], x[4]) for x in d]
d = sorted(d, key = lambda x: x[0])

# - timestamp
# - timestamp with-in 24h
# - id
# - 0 begins, 1 falls, 2 wakes
# - event minute

#print(d[:5])

m = [ [] for i in range(0, 59) ]
durations = {}

current_id = None
falls_asleep = 0

for x in d:
    if x[3] == 0:
        current_id = x[2]
        falls_asleep = None
    elif x[3] == 1:
        falls_asleep = x[1]
        if falls_asleep > 59:
            falls_asleep = 0;
    elif x[3] == 2 and current_id is not None and falls_asleep is not None:
        wakes_up = x[1]
        if wakes_up > 59:
            wakes_up = 60
        if current_id not in durations:
            durations[current_id] = 0
        durations[current_id] += wakes_up - falls_asleep
        for t in range(falls_asleep, wakes_up):
            if t >= 0 and t < 60:
                m[t] = m[t] + [current_id]

durations = sorted([(k, v) for k, v in durations.items()], key=lambda x: x[1], reverse=True)
#print(durations)

longest_sleeper = durations[0][0]
#print(longest_sleeper)
m2 = sorted([ (len([x for x in m[i] if x == longest_sleeper ]), i) for i in range(0, len(m)) ], key=lambda x:x[0], reverse=True)

print(m2[0][1] * longest_sleeper)


# task 2

from collections import Counter
m3 = [ (Counter(m[i]).most_common(1)[0], i) for i in range(0, len(m)) ]
m3 = sorted(m3, key = lambda x: x[0][1], reverse=True)
m3 = m3[0]

print(m3[0][0] * m3[1])
