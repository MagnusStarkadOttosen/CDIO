from src.client.hsvLoad import read_hsv_values
from src.client.pathfinding.GenerateNavMesh import GenerateNavMesh, coordinate_to_cell, astar, optimize_path, \
    cells_to_coordinates, escape_dead_zone


def find_path(navmesh, warped_img, robot_pos, target_pos):
    # pretty_print_navmesh(navmesh, [])
    print("sdfdjsdjkjkdsfd")
    robotCell = coordinate_to_cell(robot_pos[0], robot_pos[1], 30)

    targetCell = coordinate_to_cell(target_pos[0], target_pos[1], 30)
    print(f"robotCell: {robotCell}, targetCell: {targetCell}")
    print(f"x: {robotCell[0]}, y: {robotCell[1]}")
    print(f"asdasdas {navmesh[robotCell[1], robotCell[0]]}")
    if navmesh[robotCell[1], robotCell[0]] == 0:
        robotCell = escape_dead_zone(navmesh, robotCell)
    if navmesh[targetCell[1], targetCell[0]] == 0:
        targetCell = escape_dead_zone(navmesh, targetCell)
    path = astar(navmesh, robotCell, targetCell)
    path = astar(navmesh, robotCell, targetCell)
    # while path is None:
    #     print("try again")
    #     path = astar(navmesh, robotCell, targetCell)

    print(f"path {path}")
    optimized_path = optimize_path(navmesh, path)
    print(f"optimized path: {optimized_path}")

    coord_path = cells_to_coordinates(optimized_path, 30)

    print(f"coord_path: {coord_path}")

    return coord_path


def pretty_print_navmesh(navmesh, path):
    navmesh_copy = navmesh.copy()
    for (x, y) in path:
        navmesh_copy[y, x] = 2  # Mark the path with '2'

    for row in navmesh_copy:
        print(' '.join(str(cell) for cell in row))
