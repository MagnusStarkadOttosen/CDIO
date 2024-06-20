from src.client.pathfinding.GenerateNavMesh import cells_to_coordinates, coordinate_to_cell


grid_size = 25
x0, y0 = 350, 600


converted_coord = coordinate_to_cell(x0, y0, grid_size)
print(f"converted coords: {converted_coord}")


converted_cell = cells_to_coordinates([(converted_coord[0], converted_coord[1])], grid_size)
print(f"converted cells: {converted_cell}")

x, y = converted_cell[0][0], converted_cell[0][1]


print(x)
print(y)
print(f"original_cells: {x0}, {y0}")