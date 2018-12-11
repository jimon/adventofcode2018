import numpy as np

grid_serial_number = 1718

def getpower(x, y):
    rack_id = x + 10
    power = int((((rack_id * y + grid_serial_number) * rack_id) % 1000) / 100) - 5
    return power

grid_width = 300

grid = [ getpower(x, y) for y in range(1, grid_width + 1) for x in range(1, grid_width + 1) ]
sum_grid = [ 0 for y in range(1, grid_width + 1) for x in range(1, grid_width + 1) ]

def toi(x, y):
    return (y - 1) * grid_width + (x - 1)

def sum_or_zero(x, y):
    if x < 1 or y < 1 or x > grid_width or y > grid_width:
        return 0
    else:
        return sum_grid[toi(x, y)]

for y in range(1, grid_width + 1):
    for x in range(1, grid_width + 1):
        sum_grid[toi(x, y)] = sum_or_zero(x - 1, y) + sum_or_zero(x, y - 1) - sum_or_zero(x - 1, y - 1) + grid[toi(x, y)]


# for y in range(1, grid_width + 1):
#     print(', '.join(['%06u' % grid[toi(x, y)] for x in range(1, grid_width + 1)]))
# print('-----')
# for y in range(1, grid_width + 1):
#     print(', '.join(['%06u' % sum_grid[toi(x, y)] for x in range(1, grid_width + 1)]))

max_power = None
max_power_x = None
max_power_y = None
max_power_y = None

for y in range(1, grid_width + 1):
    print(y / (grid_width + 1))
    for x in range(1, grid_width + 1):
        for w in range(1, min(grid_width - max(x, y) + 1, 18)):
            sum_power = sum_grid[toi(x + w - 1, y + w - 1)] - sum_or_zero(x - 1, y + w - 1) - sum_or_zero(x + w - 1, y - 1) + sum_or_zero(x - 1, y - 1)
            if max_power is None or sum_power > max_power:
                max_power = sum_power
                max_power_x = x
                max_power_y = y
                max_power_w = w

print(max_power_x, max_power_y, max_power_w, max_power)
