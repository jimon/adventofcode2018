
o = set([])
r5 = 0
r5_l = 0
while True:
	r = r5 | 0x10000
	r5 = 10362650
	r5 = (((r5 + ( r        & 0xff)) & 0xffffff) * 65899) & 0xffffff
	r5 = (((r5 + ((r >>  8) & 0xff)) & 0xffffff) * 65899) & 0xffffff
	r5 = (((r5 + ((r >> 16) & 0xff)) & 0xffffff) * 65899) & 0xffffff
	if r5 in o:
		print(r5_l)
		break
	o.add(r5)
	r5_l = r5
