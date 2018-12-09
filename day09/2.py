import re

def parse(org):
	g = re.match(r"""(\d+) players; last marble is worth (\d+) points""", org)
	return (int(g.groups()[0]), int(g.groups()[1]))

class ll:
	def __init__(self, max_size):
		self.v = [0 for i in range(0, max_size)]
		self.l = [0 for i in range(0, max_size)]
		self.r = [0 for i in range(0, max_size)]
		self.v[0] = 0
		self.l[0] = 0
		self.r[0] = 0
		self.c    = 0

		self.free = 1
		for i in range(1, max_size):
			self.l[i] = i - 1
			self.r[i] = i + 1
		self.l[1] = max_size - 1
		self.r[max_size - 1] = 0

	def value(self):
		return self.v[self.c]

	def skip(self, n):
		if n > 0:
			for i in range(0, n):
				self.c = self.r[self.c]
		elif n < 0:
			for i in range(0, -n):
				self.c = self.l[self.c]

	def add(self, value):
		n = self.free
		lf = self.l[n]
		rf = self.r[n]
		self.l[rf] = lf
		self.r[lf] = rf
		self.free = rf

		l = self.c
		r = self.r[self.c]

		self.v[n] = value
		self.l[n] = l
		self.r[n] = r

		self.l[r] = n
		self.r[l] = n

		self.c = n

	def remove(self):
		n = self.c
		l = self.l[n]
		r = self.r[n]

		self.l[r] = l
		self.r[l] = r

		self.v[n] = -1
		self.l[n] = -1
		self.r[n] = -1

		lf = self.free
		rf = self.r[self.free]
		self.l[n] = lf
		self.r[n] = rf
		self.r[lf] = n
		self.l[rf] = n
		self.free = n

		self.c = r

	def print(self):
		result = []
		while True:
			result.append(self.v[index])
			index = self.r[index]
			if index == 0:
				break
		print(' '.join([('(%u)' if m == self.v[self.c] else '%u') % (m) for m in result  ]))

def game(players_count, marble_count):
	current_player = 0
	player_score = [0 for x in range(0, players_count)]
	l = ll(marble_count)

	for marble in range(1, marble_count + 1):
		if marble % 50000 == 0:
			print(float(marble) / float(marble_count))

		current_player = (current_player + 1) % players_count

		if marble % 23:
			l.skip(1)
			l.add(marble)

		else:
			l.skip(-7)

			player_score[current_player] += marble
			player_score[current_player] += l.value()

			l.remove()

	return sorted(player_score, reverse=True)[0]

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

players_count, marble_count = parse(open("input1.txt").readline())
print(game(players_count, marble_count * 100))