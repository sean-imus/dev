standard_input = "27"

eggs = int(input())

carton_size = 12

rest = eggs % carton_size
cartons_filled = eggs // carton_size

print(cartons_filled)
print(rest)