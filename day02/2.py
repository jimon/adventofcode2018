from itertools import combinations

# [x.strip() for x in open("input1.txt").readlines()] makes list of all input strings
# for x, y in combinations(..., 2) permutates all possible pair strings as AB AC ...
# if len([1 for a, b in zip(x, y) if a != b]) == 1 checks if distance between two strings is exactly one character
# [a for a, b in zip(x, y) if a == b] finds common characters between two strings
data = next(''.join([a for a, b in zip(x, y) if a == b]) for x, y in combinations([x.strip() for x in open("input1.txt").readlines()], 2) if len([1 for a, b in zip(x, y) if a != b]) == 1)

print(data)
