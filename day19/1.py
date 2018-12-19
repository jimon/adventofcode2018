
class Cpu:
	def __init__(self):
		self.r = [0, 0, 0, 0, 0, 0]
		self.ip = 0
		self.ip_mapped = None
	def setip(self, a):
		self.ip_mapped = a
	def pre(self):
		if self.ip_mapped is not None:
			self.r[self.ip_mapped] = self.ip
	def post(self):
		if self.ip_mapped is not None:
			self.ip = self.r[self.ip_mapped]
		self.ip += 1
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


cpu = Cpu()

program = [[int(y) if i > 0 else getattr(cpu, y if y != '#ip' else 'setip') for i, y in enumerate(x.strip().split())] for x in open('input1.txt').readlines()]

cpu.setip(program[0][1])
program = program[1:]

counter = 0
last_ip = 0
while True:
	#print(cpu.ip)
	counter += 1
	if counter % 100000 == 0:
		print(counter)
	cpu.pre()
	if cpu.ip >= len(program):
		break
	else:
		last_ip = cpu.ip
	#print(cpu.ip, cpu.r)
	cmd = program[cpu.ip]
	cmd[0](*cmd[1:])
	#print(cmd[0], cmd[1:])
	cpu.post()
	#print(cpu.ip, cpu.r)

print(cpu.r[0])
print(last_ip)
print(program[last_ip], cpu.r)

# task1 2520
