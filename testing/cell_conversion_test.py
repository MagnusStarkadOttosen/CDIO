from src.client.pathfinding.GenerateNavMesh import cells_to_coordinates

converted_cell = cells_to_coordinates([(11, 20)], 30)

print(converted_cell)

x, y = converted_cell[0][0], converted_cell[0][1]


print(x)
print(y)
