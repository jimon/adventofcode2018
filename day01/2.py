from itertools import cycle

freq_last = 0
freq_visited = set([freq_last])
with open("input1.txt", "r") as f:
	for delta in cycle([int(x.strip()) for x in f.readlines()]):
		freq_last += delta
		if freq_last in freq_visited:
			print("seen " + str(freq_last) + " twice")
			break
		else:
			freq_visited.add(freq_last)
