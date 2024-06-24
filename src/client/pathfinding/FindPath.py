from src.client.hsvLoad import read_hsv_values
from src.client.pathfinding.GenerateNavMesh import GenerateNavMesh, coordinate_to_cell, astar, optimize_path, \
    cells_to_coordinates, escape_dead_zone
import logging

from src.client.utilities import log_path

logging.basicConfig(filename='buffered_path.log', filemode='w',
                    format='%(asctime)s - %(message)s')

def find_path(navmesh, robot_pos, target_pos):
    # pretty_print_navmesh(navmesh, [])
    print("sdfdjsdjkjkdsfd")
    robotCell = coordinate_to_cell(robot_pos[0], robot_pos[1], 30)

    targetCell = coordinate_to_cell(target_pos[0], target_pos[1], 30)
    print(f"robotCell: {robotCell}, targetCell: {targetCell}")
    print(f"x: {robotCell[0]}, y: {robotCell[1]}")
    print(f"asdasdas {navmesh[robotCell[1], robotCell[0]]}")
    # if navmesh[robotCell[1], robotCell[0]] == 0:
    #     robotCell = escape_dead_zone(navmesh, robotCell)
    if navmesh[targetCell[1], targetCell[0]] == 0:
        targetCell = escape_dead_zone(navmesh, targetCell)
    path = astar(navmesh, robotCell, targetCell)
    # while path is None:
    #     print("try again")
    #     path = astar(navmesh, robotCell, targetCell)

    print(f"path {path}")
    optimized_path = optimize_path(navmesh, path)
    print(f"optimized path: {optimized_path}")

    coord_path = cells_to_coordinates(optimized_path, 30)

    #print(f"coord_path: {coord_path}")
    log_path(coord_path)

    return coord_path

#
# def cell_is_in_dead_zone(pos, navmesh):
#     target_cell = coordinate_to_cell(pos[0], pos[1], 30)
#     return navmesh[target_cell[1], target_cell[0]] == 0


def cell_is_in_border_zone(pos, navmesh):
    target_cell = coordinate_to_cell(pos[0], pos[1], 30)
    return navmesh[target_cell[1], target_cell[0]] == 0


def cell_is_in_cross_zone(pos, navmesh):
    target_cell = coordinate_to_cell(pos[0], pos[1], 30)
    return navmesh[target_cell[1], target_cell[0]] == 1

def pretty_print_navmesh(navmesh, path):
    navmesh_copy = navmesh.copy()
    for (x, y) in path:
        navmesh_copy[y, x] = 3  # Mark the path with '3'

    for row in navmesh_copy:
        print(' '.join(str(cell) for cell in row))
