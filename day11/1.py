def power(x, y, grid_serial_number):
    rack_id = x + 10
    power = int((((rack_id * y + grid_serial_number) * rack_id) % 1000) / 100) - 5
    return power

square_powers = [(x0, y0, sum([power(x0 + x, y0 + y, 1718) for x in range(0, 3) for y in range(0, 3)])) for x0 in range(1, 298) for y0 in range(1, 298)]
square_powers = sorted(square_powers, key = lambda x: x[2], reverse=True)

print(square_powers[0])
