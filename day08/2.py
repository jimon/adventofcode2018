#dorg = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
dorg = open("input1.txt").readlines()[0]

#2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
#A----------------------------------
#    B----------- C-----------
#                     D-----


d = [int(x) for x in dorg.split()]
#print(d)

def read_node(data, index):
	sums = 0

	if index >= len(data):
		return (index, sums)

	len_children = data[index + 0]
	len_metadata = data[index + 1]
	index += 2

	children_sums = []
	for i in range(0, len_children):
		children_sums.append(read_node(data, index))
		index = children_sums[-1][0]

	if len(children_sums) > 0:
		for i in range(0, len_metadata):
			metadata_index = data[index] - 1
			if metadata_index >= 0 and metadata_index < len(children_sums):
				sums += children_sums[metadata_index][1]
			index += 1
	else:
		for i in range(0, len_metadata):
			sums += data[index]
			index += 1

	return (index, sums)


print(read_node(d, 0))
