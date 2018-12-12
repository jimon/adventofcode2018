d = [x.strip() for x in open("input1.txt").readlines() if len(x.strip()) > 0]

def ltot(l):
	return (l[0], l[1], l[2], l[3], l[4])

def cfgtoi(cfg):
	return 1 if cfg == '#' else 0 

state = [cfgtoi(x) for x in d[0][len('initial state: '):]]
rules = {ltot([cfgtoi(x) for x in l[0:5]]): cfgtoi(l[9:]) for l in d[1:]}

def get(state, i):
	return state[i] if i >= 0 and i < len(state) else 0

def sim(state, zero_index, rules):
	sl = []
	sm = []
	sr = []
	for i in range(-4, len(state) + 5):
		s = ltot([get(state, i2) for i2 in range(i - 2, i + 3)])
		n = rules[s] if s in rules else 0
		if i < 0:
			sl.append(n)
		elif i >= 0 and i < len(state):
			sm.append(n)
		else:
			sr.append(n)

	left_delta = None
	for i in range(0, 4):
		if sl[i]:
			left_delta = i - 4
			sm = sl[i:] + sm
	if left_delta is not None:
		zero_index += left_delta

	right_delta = None
	for i in range(0, 4):
		if sr[i]:
			right_delta = i
	if right_delta is not None:
		sm = sm + sr[:right_delta + 1]
	return sm, zero_index

def print_debug(iteration, state, zero_index):
	print('%02u: %s (%u)' % (iteration, ''.join(['#' if x == 1 else '.' for x in state]), zero_index))

zero_index = 0
print_debug(0, state, zero_index)
for i in range(1, 21):
	state, zero_index = sim(state, zero_index, rules)
	print_debug(i, state, zero_index)

value = 0
for i, x in enumerate(state):
	if x:
		value += i + zero_index
print(value)
