import re

def parse(org):
	g = re.match(r"""(\d+) players; last marble is worth (\d+) points""", org)
	return (int(g.groups()[0]), int(g.groups()[1]))

def ll_to_array(marbles):
	current = 0
	r = []
	while True:
		r.append(marbles[current][0])
		current = marbles[current][2]
		if marbles[current][2] == 0:
			r.append(marbles[current][0])
			break
	return r

def skip_N(marbles, index, skip):
	if skip > 0:
		for i in range(0, skip):
			index = marbles[index][2]
	elif skip < 0:
		for i in range(0, -skip):
			index = marbles[index][1]
	return index

def verify_linked_list(marbles):
	current = 0
	elements_right = 0

	while True:
		current = marbles[current][2]
		elements_right += 1
		if current == 0:
			break

	current = 0
	elements_left = 0

	while True:
		current = marbles[current][1]
		elements_left += 1
		if current == 0:
			break

	assert(elements_left == elements_right)


def game(players_count, marble_count):
	current_player = 0
	current_index = 0
	player_score = [0 for x in range(0, players_count)]
	marbles = [(None, None, None) for i in range(0, marble_count + 1)]
	marbles[0] = (0, 0, 0)
	next_free = 1
	verify_linked_list(marbles)

	for marble in range(1, marble_count + 1):
		current_player = (current_player + 1) % players_count

		if marble % 23:
			index = skip_N(marbles, current_index, 1)

			left_index  = index
			right_index = marbles[index][2]

			#print(index, left_index, right_index, next_free)

			marbles[ left_index  ] = (marbles[ left_index ][0], marbles[ left_index ][1], next_free)
			marbles[ right_index ] = (marbles[ right_index ][0], next_free, marbles[ right_index ][2])
			marbles[ next_free   ] = (marble, left_index, right_index)
			verify_linked_list(marbles)

			current_index = next_free

			next_free = None
			for i in range(0, len(marbles)):
				if marbles[i][0] == None:
					next_free = i
					break

		else:
			current_index = skip_N(marbles, current_index, -7)
			#print(marbles[index])

			player_score[current_player] += marble
			player_score[current_player] += marbles[current_index][0]

			left_index  = marbles[current_index][1]
			right_index = marbles[current_index][2]

			marbles[left_index] =  (marbles [left_index][0],  marbles[left_index][1], right_index)
			marbles[right_index] = (marbles[right_index][0],  left_index,             marbles[right_index][2])

			#marbles[current_index] = (None, None, None)
			verify_linked_list(marbles)

			#print(marbles)
			#print(ll_to_array(marbles))

			next_free = current_index

			# current_index = left_index


			#del marbles[current_marble]

		#print("[%u] %s" % (current_player + 1, ''.join([ ('(%u)' if i == current_index else ' %u ') % (m) for i, m in enumerate(ll_to_array(marbles))  ])))
		#print(marbles)

	return sorted(player_score, reverse=True)[0]

print(game(9, 25))

test_data = [
	(9, 25, 32),
	(10, 1618, 8317),
	(13, 7999, 146373),
	(17, 1104, 2764),
	(21, 6111, 54718),
	(30, 5807, 37305),
]

for t in test_data:
	print(game(t[0], t[1]) == t[2])

#players_count, marble_count = parse(open("input1.txt").readline())
#print(game(players_count, marble_count))