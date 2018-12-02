from itertools import compress, combinations

def dist(x, y):
	assert(len(x) == len(y))
	return sum([1 for i in range(0, len(x)) if x[i] != y[i]])

input_strings = [list(x.strip()) for x in open("input1.txt").readlines()]
data = next(''.join([x[i] for i in range(0, len(x)) if x[i] == y[i]]) for x, y in combinations(input_strings, 2) if dist(x, y) == 1)

print(data)
