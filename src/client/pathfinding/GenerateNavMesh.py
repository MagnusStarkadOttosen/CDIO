
import cv2
import numpy as np


def GenerateNavMesh(image, hsv_values):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape

    # Define the grid size for the navmesh
    grid_size = 30
    buffer_size = 100

    # Find 
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([hsv_values['LowerH'], hsv_values['LowerS'], hsv_values['LowerV']])
    upper_bound = np.array([hsv_values['UpperH'], hsv_values['UpperS'], hsv_values['UpperV']])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    inverted_mask = cv2.bitwise_not(mask)


    # Create an empty navmesh grid
    navmesh = np.zeros((height // grid_size, width // grid_size), dtype=np.uint8)

    # Create a buffer around the black areas
    kernel = np.ones((buffer_size, buffer_size), np.uint8)
    buffered_mask = cv2.erode(inverted_mask, kernel, iterations=2)

    # Fill the navmesh grid based on the buffered_mask
    for y in range(0, height, grid_size):
        for x in range(0, width, grid_size):
            # Skip cells near the edges of the image to create a buffer
            if y < buffer_size or y + grid_size > height - buffer_size or x < buffer_size or x + grid_size > width - buffer_size:
                continue
            cell = buffered_mask[y:y + grid_size, x:x + grid_size]
            # Calculate the percentage of the cell that is white
            white_pixels = np.sum(cell == 255)
            total_pixels = cell.size
            if white_pixels / total_pixels >= 0.75:
                navmesh[y // grid_size, x // grid_size] = 1

    # Invert the mesh to work with a star
    inverted_navmesh = np.logical_not(navmesh).astype(np.uint8)

    return inverted_navmesh

# Converts the coordinates from the image to the cell
def coordinate_to_cell(x, y, grid_size):
    cell_x = x // grid_size
    cell_y = y // grid_size
    return cell_x, cell_y

# Converts the list of cells from a star to a list of coordinates
def cells_to_coordinates(cells, grid_size):
    coordinates = []
    for cell_x, cell_y in cells:
        top_left = (cell_x * grid_size, cell_y * grid_size)
        bottom_right = ((cell_x + 1) * grid_size, (cell_y + 1) * grid_size)
        coordinates.append((top_left, bottom_right))
    return coordinates