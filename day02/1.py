from collections import Counter

# list of lists which contain count of single character occurences in a string
data = [[v for k, v in Counter(list(x.strip())).items()] for x in open("input1.txt").readlines()]

print(sum([1 for x in data if 2 in x]) * sum([1 for x in data if 3 in x]))