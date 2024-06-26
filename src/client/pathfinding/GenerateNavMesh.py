
from collections import deque
import heapq
import cv2
import numpy as np

from src.CONSTANTS import GRID_SIZE
from src.client.utilities import log_path

WALKABLE_INDEX = 2
OBSTACLE_INDEX = 1

def GenerateNavMesh(image, hsv_values):
    """
    Generates a navigation mesh from an image. The NavMesh is a grid of 25x25mm cells.
    0 indicates the buffer around the walls
    1 indicates the buffer around the obstacle
    2 indicates the area the robot can move

    Parameters
    ----------
    image : numpy.ndarray
        The input image.
    hsv_values : dict
        Contains the HSV values for the mask (red for wall).

    Returns
    -------
    numpy.ndarray
        The generated navigation mesh.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape

    # Define the grid size for the navmesh
    grid_size = GRID_SIZE
    buffer_size = 185
    buffer_edge = 150

    # Mask everything but the red area
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([hsv_values['LowerH'], hsv_values['LowerS'], hsv_values['LowerV']])
    upper_bound = np.array([hsv_values['UpperH'], hsv_values['UpperS'], hsv_values['UpperV']])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    inverted_mask = cv2.bitwise_not(mask)

    # Set the edge pixels to white. This is to prevent the rogue red pixels from the edge of the image messing with the navmesh.
    edge_size = 20
    inverted_mask[:edge_size, :] = 255 # top wall
    inverted_mask[-edge_size:, :] = 255 # bottom wall
    inverted_mask[:, :edge_size] = 255 # left wall
    inverted_mask[:, -edge_size:] = 255 # right wall

    # Remove rogue pixels from orange ball spillover
    kernel_size = 15
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    closed_mask = cv2.morphologyEx(inverted_mask, cv2.MORPH_CLOSE, kernel)

    # Create an empty navmesh grid
    navmesh = np.zeros((height // grid_size, width // grid_size), dtype=np.uint8)

    # Create a buffer around the black areas by eroding the mask
    kernel = np.ones((buffer_size, buffer_size), np.uint8)
    buffered_mask = cv2.erode(closed_mask, kernel, iterations=2)

    # Fill the navmesh grid based on the buffered_mask
    for y in range(0, height, grid_size):
        for x in range(0, width, grid_size):
            # Skip cells near the edges of the image to create a buffer
            if y < buffer_edge or y + grid_size > height - buffer_edge or x < buffer_edge or x + grid_size > width - buffer_edge:
                continue
            cell = buffered_mask[y:y + grid_size, x:x + grid_size]
            # Calculate the percentage of the cell that is white
            white_pixels = np.sum(cell == 255)
            total_pixels = cell.size
            if white_pixels / total_pixels >= 0.75:
                navmesh[y // grid_size, x // grid_size] = WALKABLE_INDEX
            else:
                navmesh[y // grid_size, x // grid_size] = OBSTACLE_INDEX


    return navmesh

# Converts the coordinates from the image to the cell
def coordinate_to_cell(x, y, grid_size):
    """
    Converts coordinates from the image to the corresponding cell in the navigation mesh.

    Parameters
    ----------
    x : int
        The x-coordinate.
    y : int
        The y-coordinate.
    grid_size : int
        The size of each cell in the grid.

    Returns
    -------
    tuple
        The cell coordinates (cell_x, cell_y).
    """
    cell_x = x // grid_size
    cell_y = y // grid_size
    return cell_x, cell_y

# Converts the list of cells from a star to a list of coordinates
def cells_to_coordinates(cells, grid_size):
    """
    Converts a list of cells from the navigation mesh to coordinates.

    Parameters
    ----------
    cells : list
        The list of cell coordinates.
    grid_size : int
        The size of each cell in the grid.

    Returns
    -------
    list
        The list of coordinates corresponding to the cells.
    """
    print("cells:", cells, "grid_size:", grid_size)
    coordinates = [(x*grid_size,y*grid_size) for x, y in cells]
    return coordinates

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(navmesh, start, goal):
    """
    Finds a path from start to goal using the A* algorithm.

    Parameters
    ----------
    navmesh : numpy.ndarray
        The navigation mesh.
    start : tuple
        The starting cell (x, y).
    goal : tuple
        The goal cell (x, y).

    Returns
    -------
    list
        A list of cells representing the path from start to goal, or None if no path is found.
    """
    # Priority queue to store (cost, current_node)
    open_set = []
    heapq.heappush(open_set, (0, start))

    # Dictionaries to store the cost from start to each node and the path
    g_costs = {start: 0}
    came_from = {start: None}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct the path
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        # Get neighbors
        neighbors = [
            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1),
            (current[0] + 1, current[1] + 1),
            (current[0] - 1, current[1] - 1),
            (current[0] + 1, current[1] - 1),
            (current[0] - 1, current[1] + 1)
        ]

        for neighbor in neighbors:
            if 0 <= neighbor[1] < navmesh.shape[0] and 0 <= neighbor[0] < navmesh.shape[1]:
                if navmesh[neighbor[1], neighbor[0]] == WALKABLE_INDEX:  # Check if neighbor is walkable
                    tentative_g_cost = g_costs[current] + 1
                    if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:
                        g_costs[neighbor] = tentative_g_cost
                        f_cost = tentative_g_cost + heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_cost, neighbor))
                        came_from[neighbor] = current
    print("No path found.")
    return None  # Path not found

def is_walkable(navmesh, start, end):
    x0, y0 = start
    x1, y1 = end
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        if navmesh[y0, x0] == 0 or navmesh[y0, x0] == 1:
            return False
        if (x0, y0) == (x1, y1):
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return True

def optimize_path(navmesh, path):
    """
    Optimizes the path by removing unnecessary waypoints.
    Allowing the robot to travel in a straight line without starting and stopping

    Parameters
    ----------
    navmesh : numpy.ndarray
        The navigation mesh.
    path : list
        The initial path.

    Returns
    -------
    list
        The optimized path.
    """
    if path is None:
        return path

    optimized_path = [path[0]]
    i = 0

    while i < len(path) - 1:
        for j in range(len(path) - 1, i, -1):
            if is_walkable(navmesh, path[i], path[j]):
                optimized_path.append(path[j])
                i = j
                break
        i += 1
    return optimized_path

# This find the nearest walkable cells using breath first
def escape_dead_zone(navmesh, start):
    """
    Finds the nearest walkable cell using breadth-first search.

    Parameters
    ----------
    navmesh : numpy.ndarray
        The navigation mesh.
    start : tuple
        The starting cell (x, y).

    Returns
    -------
    tuple
        The coordinates of the nearest walkable cell.
    """
    height, width = navmesh.shape
    visited = set()
    queue = deque([start])

    while queue:
        x, y = queue.popleft()
        if (x, y) not in visited:
            visited.add((x, y))
            if 0 <= y < height and 0 <= x < width and navmesh[int(y), int(x)] == WALKABLE_INDEX:
                return x, y

            neighbors = [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
                (x + 1, y + 1),
                (x - 1, y - 1),
                (x + 1, y - 1),
                (x - 1, y + 1)
            ]
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)

    return None