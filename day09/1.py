import re

def parse(org):
	g = re.match(r"""(\d+) players; last marble is worth (\d+) points""", org)
	return (int(g.groups()[0]), int(g.groups()[1]))

def game(players_count, marble_count):
	current_player = 0
	current_marble = 0
	player_score = [0 for x in range(0, players_count)]
	marbles = [0]

	for marble in range(1, marble_count + 1):
		current_player = (current_player + 1) % players_count

		if marble % 23:
			current_marble = ((current_marble + 1) % len(marbles)) + 1
			marbles.insert(current_marble, marble)
		else:
			current_marble = ((current_marble - 7) % len(marbles))
			player_score[current_player] += marble
			player_score[current_player] += marbles[current_marble]
			del marbles[current_marble]

		#print("[%u] %s" % (current_player + 1, ''.join([ ('(%u)' if i == current_marble else ' %u ') % (m) for i, m in enumerate(marbles)  ])))

	return sorted(player_score, reverse=True)[0]



# test_data = [
# 	(9, 25, 32),
# 	(10, 1618, 8317),
# 	(13, 7999, 146373),
# 	(17, 1104, 2764),
# 	(21, 6111, 54718),
# 	(30, 5807, 37305),
# ]

# for t in test_data:
# 	print(game(t[0], t[1]) == t[2])

players_count, marble_count = parse(open("input1.txt").readline())
print(game(players_count, marble_count))