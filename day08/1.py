#dorg = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

#2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
#A----------------------------------
#    B----------- C-----------
#                     D-----

dorg = open("input1.txt").readlines()[0]
d = [int(x) for x in dorg.split()]
#print(d)

all_metadata = 0

def read_node(data, index):
	global all_metadata

	if index >= len(data):
		return index

	#print('read node at', index)
	len_children = data[index + 0]
	len_metadata = data[index + 1]
	index += 2

	for i in range(0, len_children):
		#print('read children at', index)
		index = read_node(data, index)

	for i in range(0, len_metadata):
		#print('read metadata at', index)
		all_metadata += data[index]
		index += 1

	return index


read_node(d, 0)

print(all_metadata)