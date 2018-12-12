d = [x.strip() for x in open("input1.txt").readlines() if len(x.strip()) > 0]

#print(d)

def cfgtoi(cfg):
	return 1 if x == '#' else 0 

state = [cfgtoi(x) for x in d[0][len('initial state: '):]]

k = [[cfgtoi(x) for x in l[0:5] + l[9:]] for l in d[1:]]

print(k)
