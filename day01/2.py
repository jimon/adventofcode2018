from itertools import cycle

freq_last = 0
freq_visited = set([freq_last])
for delta in cycle([int(x.strip()) for x in open("input1.txt").readlines()]):
	freq_last += delta
	if freq_last in freq_visited:
		print("seen " + str(freq_last) + " twice")
		break
	else:
		freq_visited.add(freq_last)
