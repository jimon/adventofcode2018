from collections import Counter

# "for x in open("input1.txt").readlines()" makes a generator that reads all lines one by one
# "Counter(x.strip()).values()" counts occurences of every symbol in a line and return array of how many time every symbol occured
# "set( )" only leaves unique occurences, so if two symbols occured twice we only leave one 2
data = Counter(v for x in open("input1.txt").readlines() for v in set(Counter(x.strip()).values()))

print(data[2] * data[3])
