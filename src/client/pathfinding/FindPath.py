from src.CONSTANTS import GRID_SIZE
from src.client.hsvLoad import read_hsv_values
from src.client.pathfinding.GenerateNavMesh import GenerateNavMesh, coordinate_to_cell, astar, optimize_path, \
    cells_to_coordinates, escape_dead_zone
import logging

from src.client.utilities import log_path

logging.basicConfig(filename='buffered_path.log', filemode='w',
                    format='%(asctime)s - %(message)s')


def find_path(navmesh, robot_pos, target_pos):

    robotCell = coordinate_to_cell(robot_pos[0], robot_pos[1], GRID_SIZE)

    targetCell = coordinate_to_cell(target_pos[0], target_pos[1], GRID_SIZE)
    print(f"robotCell: {robotCell}, targetCell: {targetCell}")

    if navmesh[robotCell[1], robotCell[0]] in (0, 1):
        robotCell = escape_dead_zone(navmesh, robotCell)

    if navmesh[targetCell[1], targetCell[0]] in (0, 1):
        targetCell = escape_dead_zone(navmesh, targetCell)

    path = astar(navmesh, robotCell, targetCell)

    optimized_path = optimize_path(navmesh, path)
    print(f"optimized path: {optimized_path}")

    coord_path = cells_to_coordinates(optimized_path, GRID_SIZE)

    if coord_path is not None:
        log_path(coord_path)
    else:
        log_path("No path found.")

    return coord_path


#
# def cell_is_in_dead_zone(pos, navmesh):
#     target_cell = coordinate_to_cell(pos[0], pos[1], GRID_SIZE)
#     return navmesh[target_cell[1], target_cell[0]] == 0


def pretty_print_navmesh(navmesh, path, robot_pos):
    pos_cell = coordinate_to_cell(robot_pos[0], robot_pos[1], GRID_SIZE)
    navmesh_copy = navmesh.copy()

    if path is not None:
        for (x, y) in path:
            navmesh_copy[y, x] = 3  # Mark the path with '3'

    navmesh_copy[pos_cell[1], pos_cell[0]] = 4
    # navmesh_copy[int(robot_pos[1]), int(robot_pos[0])] = 4
    symbols = {
        0: 'B',
        1: 'C',
        2: '.',
        3: 'P',
        4: 'R'
    }

    for row in navmesh_copy:
        print(' '.join(symbols[cell] for cell in row))
