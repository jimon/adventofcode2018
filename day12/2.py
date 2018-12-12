
# from part 1, on iteration 108 the pattern stops changing

idata = "......................................##.#....##.#....##.#....##.#....##.#....##.#.....##.#........##.#....##.#.....###.#....###.#....###.#....###.#....##.#....##.#....##.#....##.#....###.#....##.#....##.#"

data = [1 if x == '#' else 0 for x in idata]
print(data)

value = 0
for i, x in enumerate(data):
	if x:
		value += i + (50000000000 - 108)
print(value)