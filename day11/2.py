import numpy as np

grid_serial_number = 18

def getpower(x, y, grid_serial_number):
    rack_id = x + 10
    power = int((((rack_id * y + grid_serial_number) * rack_id) % 1000) / 100) - 5
    return power

grid = np.array([ getpower(x, y, grid_serial_number) for y in range(1, 301) for x in range(1, 301) ])

max_power = None
max_power_x = None
max_power_y = None
max_power_w = None

for y0 in range(1, 10):
    print((y0 * 300 + 0) / (300 * 300 + 300))
    for x0 in range(1, 10):
        for w in range(0, 20):#300 - max(x0, y0) + 1):
            if x0 + w > 300 or y0 + w > 300:
                continue
            assert(x0 + w <= 300)
            assert(y0 + w <= 300)

            power = np.sum([np.sum(grid[y*300+x0:x0+w+1]) for y in range(y0, y0 + w + 1)])
            print(power)

            if max_power is None or power > max_power:
                max_power = power
                max_power_x = x0
                max_power_y = y0
                max_power_w = w

print(max_power_x, max_power_y, max_power_w, max_power)


#square_powers = [(x0, y0, w, sum([power(x0 + x, y0 + y, 1718) for x in range(0, 3) for y in range(0, 3)])) for x0 in range(1, 298) for y0 in range(1, 298)]
#square_powers = sorted(square_powers, key = lambda x: x[2], reverse=True)

#print(square_powers[0])
