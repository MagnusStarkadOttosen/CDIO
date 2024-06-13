import math
import heapq

# Define the Cell class
class Cell:
	def __init__(self):
		self.parent_i = 0 # Parent cell's row index
		self.parent_j = 0 # Parent cell's column index
		self.f = float('inf') # Total cost of the cell (g + h)
		self.g = float('inf') # Cost from start to this cell
		self.h = 0 # Heuristic cost from this cell to destination

# Define the size of the grid
ROW = 12
COL = 18

# Check if a cell is valid (within the grid)
def is_valid(col, row):
	return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

# Check if a cell is unblocked
def is_unblocked(grid, col, row):
	return grid[col][row] == 0

# Check if a cell is the destination
def is_destination(row, col, dest):
	return col == dest[0] and row == dest[1] 

# Calculate the heuristic value of a cell (Euclidean distance to destination)
def calculate_h_value(col,row,dest):
	return ((col - dest[0]) ** 2 + (row - dest[1]) ** 2) ** 0.5

# Trace the path from source to destination
def trace_path(cell_details, dest):
	path = []
	col = dest[0]
	row = dest[1]

	# Trace the path from destination to source using parent cells
	while not (cell_details[col][row].parent_i == col and cell_details[col][row].parent_j == row):
		path.append((col, row))
		# get the parent cell's indices
		temp_col = cell_details[col][row].parent_i
		temp_row = cell_details[col][row].parent_j
		# Move to the parent cell
		col = temp_col
		row = temp_row
		

	# Add the source cell to the path
	path.append((col, row))
	# Reverse the path to get the path from source to destination
	path.reverse()
	return path

# 	Optimize the path by removing unnecessary points
def optimize_path(path):
    if not path:
        return []

    optimized_path = [path[0]] # Add the first point
    current_direction = get_direction(path[0], path[1])

    for i in range(1, len(path) - 1):
        next_direction = get_direction(path[i], path[i + 1])
        if next_direction != current_direction:
            optimized_path.append(path[i])
            current_direction = next_direction

    optimized_path.append(path[-1])  # Add the last point
    return optimized_path

def get_direction(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    if dx == 0:
        return 'vertical'
    elif dy == 0:
        return 'horizontal'
    elif abs(dx) == abs(dy):
        return 'diagonal'
    else:
        return 'none'


# Implement the A* search algorithm
def a_star_search(grid, src, dest):
	# Check if the source and destination are valid
	if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
		print("Source or destination is invalid")
		return

	# Check if the source and destination are unblocked
	if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
		print("Source or the destination is blocked")
		return

	# Check if we are already at the destination
	if is_destination(src[0], src[1], dest):
		print("We are already at the destination")
		return

	# Initialize the closed list (visited cells)
	closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
	# Initialize the details of each cell
	cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

	# Initialize the start cell details
	i = src[0]
	j = src[1]
	cell_details[i][j].f = 0
	cell_details[i][j].g = 0
	cell_details[i][j].h = 0
	cell_details[i][j].parent_i = i
	cell_details[i][j].parent_j = j

	# Initialize the open list (cells to be visited) with the start cell
	open_list = []
	heapq.heappush(open_list, (0.0, i, j))

	# Initialize the flag for whether destination is found
	found_dest = False

	# Main loop of A* search algorithm
	while len(open_list) > 0:
		# Pop the cell with the smallest f value from the open list
		p = heapq.heappop(open_list)

		# Mark the cell as visited
		i = p[1]
		j = p[2]
		closed_list[i][j] = True

		# For each direction, check the successors
		directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
		for dir in directions:
			new_i = i + dir[0]
			new_j = j + dir[1]

			# If the successor is valid, unblocked, and not visited
			if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
				# If the successor is the destination
				if is_destination(new_i, new_j, dest):
					# Set the parent of the destination cell
					cell_details[new_i][new_j].parent_i = i
					cell_details[new_i][new_j].parent_j = j
					print("The destination cell is found")
					# Trace the path from source to destination
					full_path = trace_path(cell_details, (new_i, new_j))
					optimized_path = optimize_path(full_path)
					return optimized_path
				else:
					# Calculate the new f, g, and h values
					g_new = cell_details[i][j].g + 1.0
					h_new = calculate_h_value(new_i, new_j, dest)
					f_new = g_new + h_new

					# If the cell is not in the open list or the new f value is smaller
					if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
						# Add the cell to the open list
						heapq.heappush(open_list, (f_new, new_i, new_j))
						# Update the cell details
						cell_details[new_i][new_j].f = f_new
						cell_details[new_i][new_j].g = g_new
						cell_details[new_i][new_j].h = h_new
						cell_details[new_i][new_j].parent_i = i
						cell_details[new_i][new_j].parent_j = j

	# If the destination is not found after visiting all cells
	if not found_dest:
		print("Failed to find the destination cell")
		return None
	