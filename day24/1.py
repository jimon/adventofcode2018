import re

rs1 = re.compile(r"""^Immune System:$""")
rs2 = re.compile(r"""^Infection:$""")
rl = re.compile(r"""^(\d+) units each with (\d+) hit points(?: \((.+)\))? with an attack that does (\d+) (\w+) damage at initiative (\d+)$""")
re = re.compile(r"""^(weak|immune) to ([\w\s,]+)(?:; (weak|immune) to ([\w\s,]+))?$""")

d = [x.strip() for x in open('input1.txt').readlines() if len(x.strip()) > 0]

class Group:
	def __init__(self, config_line):
		g = rl.match(config_line).groups()
		self.count = g[0]
		self.hp = g[1]
		self.weak_to = []
		self.immute_to = []
		self.attack = g[3]
		self.attack_demage = g[4]
		self.initiative = g[5]
		if g[2]:
			g2 = re.match(g[2]).groups()
			if g2[0] == 'weak':
				self.weak_to = g2[1].split()
			elif g2[0] == 'immune':
				self.immute_to = g2[1].split()
			if g2[2] == 'weak':
				self.weak_to = g2[3].split()
			elif g2[2] == 'immune':
				self.immute_to = g2[3].split()


groups_immune_system = []
groups_infection = []

current_group = None
for x in d:
	if rs1.match(x):
		current_group = groups_immune_system
	elif rs2.match(x):
		current_group = groups_infection
	else:
		current_group.append(Group(x))


print(groups_infection)

