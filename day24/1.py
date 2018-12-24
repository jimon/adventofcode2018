import re

rs1 = re.compile(r"""^Immune System:$""")
rs2 = re.compile(r"""^Infection:$""")
rl = re.compile(r"""^(\d+) units each with (\d+) hit points(?: \((.+)\))? with an attack that does (\d+) (\w+) damage at initiative (\d+)$""")
re = re.compile(r"""^(weak|immune) to ([\w\s,]+)(?:; (weak|immune) to ([\w\s,]+))?$""")

class Group:
	def __init__(self, index, kind, config_line):
		g = rl.match(config_line).groups()

		self.index          = index
		self.in_group_index = 0
		self.kind           = kind
		self.count          = int(g[0])
		self.hp             = int(g[1])
		self.weak_to        = []
		self.immune_to      = []
		self.attack_damage  = int(g[3])
		self.attack_type    = g[4]
		self.initiative     = int(g[5])

		if g[2]:
			g2 = re.match(g[2]).groups()
			if g2[0] == 'weak':
				self.weak_to = g2[1].split(',')
			elif g2[0] == 'immune':
				self.immune_to = g2[1].split(',')
			if g2[2] == 'weak':
				assert(len(self.weak_to) == 0)
				self.weak_to = g2[3].split(',')
			elif g2[2] == 'immune':
				assert(len(self.immune_to) == 0)
				self.immune_to = g2[3].split(',')
			self.weak_to = [x.strip() for x in self.weak_to if len(x.strip()) > 0]
			self.immune_to = [x.strip() for x in self.immune_to if len(x.strip()) > 0]

	@property
	def immune_system(self):
		return self.kind == 0

	@property
	def infection(self):
		return self.kind == 1

	@property
	def alive(self):
		return self.count > 0

	@property
	def dead(self):
		return self.count <= 0

	@property
	def effective_power(self):
		return self.count * self.attack_damage

	def will_deal_damage(self, another_group):
		damage = self.effective_power
		if self.attack_type in another_group.immune_to:
			damage = 0
		elif self.attack_type in another_group.weak_to:
			damage *= 2
		return damage

	def attack(self, another_group):
		damage = self.will_deal_damage(another_group)
		damage //= another_group.hp
		units_killed = damage
		#units_killed = int(damage / another_group.hp)
		if units_killed > another_group.count:
			units_killed = another_group.count
		another_group.count -= units_killed
		return units_killed

def parse(filename):
	groups = []
	current_group_kind = None
	for x in [x.strip() for x in open(filename).readlines() if len(x.strip()) > 0]:
		if rs1.match(x):
			current_group_kind = 0
		elif rs2.match(x):
			current_group_kind = 1
		else:
			groups.append(Group(len(groups), current_group_kind, x))

	c = 0
	for g in groups:
		if g.immune_system:
			c += 1
			g.in_group_index = c
	c = 0
	for g in groups:
		if g.infection:
			c += 1
			g.in_group_index = c
	return groups

def play_game(groups):
	c = 0


	while (len([1 for g in groups if g.immune_system and g.alive]) > 0) and (len([1 for g in groups if g.infection and g.alive]) > 0):
		c += 1

		will_be_attacked = set([])
		will_attack = {}

		for g in sorted(groups, key=lambda g: (g.effective_power, g.initiative), reverse=True):
			if g.dead:
				continue

			k = [g2 for g2 in groups if g.kind != g2.kind and g2.alive and g2.index not in will_be_attacked and g.will_deal_damage(g2) > 0]
			if len(k) == 0:
				continue
			k = sorted(k, key=lambda g2: (g.will_deal_damage(g2), g2.effective_power, g2.initiative), reverse=True)

			i2 = k[0].index
			will_attack[g.index] = i2
			will_be_attacked.add(i2)

		if c % 1000 == 0:
			print('                                                                      ', end='\r')
			print(c, sum([g.count for g in groups]), will_attack, end = '\r')

		attack_turns = [g.index for g in sorted(groups, key=lambda g: g.initiative, reverse=True)]
		for i in attack_turns:
			if i in will_attack:
				groups[i].attack(groups[will_attack[i]])


groups = parse('inputk.txt')
play_game(groups)

print('------------------------------------')
print('are we still valid', sum([g.count for g in groups]) == 5216)

groups = parse('input1.txt')
play_game(groups)
print('------------------------------------')
print('result', sum([g.count for g in groups]))
# 11264 is too high
# 9737 is too high
# 8681 is too low