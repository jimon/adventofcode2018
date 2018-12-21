import matplotlib.pyplot as plt
d = [int(x.strip()) for x in open('data.txt').readlines()]
plt.plot(d)
plt.show()
