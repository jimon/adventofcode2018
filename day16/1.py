
class Cpu:
	def __init__(self):
		self.r = [0, 0, 0, 0]
		self.op = [
			self.addr,
			self.addi,
			self.mulr,
			self.muli,
			self.banr,
			self.bani,
			self.borr,
			self.bori,
			self.setr,
			self.seti,
			self.gtir,
			self.gtri,
			self.gtrr,
			self.eqir,
			self.eqri,
			self.eqrr,
		]
	def addr(self, a, b, c):
		self.r[c] = self.r[a] + self.r[b]
	def addi(self, a, b, c):
		self.r[c] = self.r[a] + b
	def mulr(self, a, b, c):
		self.r[c] = self.r[a] * self.r[b]
	def muli(self, a, b, c):
		self.r[c] = self.r[a] * b
	def banr(self, a, b, c):
		self.r[c] = self.r[a] & self.r[b]
	def bani(self, a, b, c):
		self.r[c] = self.r[a] & b
	def borr(self, a, b, c):
		self.r[c] = self.r[a] | self.r[b]
	def bori(self, a, b, c):
		self.r[c] = self.r[a] | b
	def setr(self, a, b, c):
		self.r[c] = self.r[a]
	def seti(self, a, b, c):
		self.r[c] = a
	def gtir(self, a, b, c):
		self.r[c] = 1 if a > self.r[b] else 0
	def gtri(self, a, b, c):
		self.r[c] = 1 if self.r[a] > b else 0
	def gtrr(self, a, b, c):
		self.r[c] = 1 if self.r[a] > self.r[b] else 0
	def eqir(self, a, b, c):
		self.r[c] = 1 if a == self.r[b] else 0
	def eqri(self, a, b, c):
		self.r[c] = 1 if self.r[a] == b else 0
	def eqrr(self, a, b, c):
		self.r[c] = 1 if self.r[a] == self.r[b] else 0
	def test(self, r0, r1, opcode):
		works = []
		for i, f in enumerate(self.op):
			self.r[0] = r0[0]
			self.r[1] = r0[1]
			self.r[2] = r0[2]
			self.r[3] = r0[3]
			f(*opcode[1:])
			if self.r[0] == r1[0] and self.r[1] == r1[1] and self.r[2] == r1[2] and self.r[3] == r1[3]:
				works.append(i)
		return works

cpu = Cpu()

import re
d = [x.strip() for x in open('input1.txt').readlines()]

match_a = re.compile(r"""Before:\s*\[(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\]""")
match_b = re.compile(r"""(\d+)\s+(\d+)\s+(\d+)\s+(\d+)""")
match_c = re.compile(r"""After:\s*\[(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\]""")

counter = 0
for i in range(0, int(len(d) / 4)):
	a=[int(x) for x in match_a.match(d[i*4+0]).groups()]
	b=[int(x) for x in match_b.match(d[i*4+1]).groups()]
	c=[int(x) for x in match_c.match(d[i*4+2]).groups()]
	w = cpu.test(a, c, b)
	if len(w) >= 3:
		#print(w)
		counter += 1

print(counter)

# 569 too low