with open("input1.txt", "r") as f:
	print(sum([int(x.strip()) for x in f.readlines()]))