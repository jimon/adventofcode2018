
def calc(r0):
	r5 = 0
	c = 0
	while r5 != r0:
		r = r5 | 0x10000
		r5 = 10362650
		r5 = (((r5 + ( r        & 0xff)) & 0xffffff) * 65899) & 0xffffff
		r5 = (((r5 + ((r >>  8) & 0xff)) & 0xffffff) * 65899) & 0xffffff
		r5 = (((r5 + ((r >> 16) & 0xff)) & 0xffffff) * 65899) & 0xffffff
		c += 1
		if c >= 4:
			return None
	return c

r0 = 3935446
while True:
	r0 += 1
	c = calc(r0)
	if c is not None:
		print(r0, c)
	elif r0 % 10000 == 0:
		print(r0, '\r', end='')
