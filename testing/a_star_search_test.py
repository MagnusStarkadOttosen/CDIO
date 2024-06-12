

    # Define the source and destination cells
from src.client.search_targetpoint.a_star_search import find_path


src = [3, 4]
dest = [1, 2]  

# Define the grid (1 for unblocked, 0 for blocked)
grid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1,1,1,1,1,1,1,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1,0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1,0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1,0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1,1,1,1,1,1,1,1],
    ]

# Run the A* search algorithm
asdf = find_path(grid, src, dest)
if asdf:
    for(i, j) in asdf:
       grid[j][i] = 3
    for row in grid:
        print("".join(str(cell) for cell in row))
print(asdf)
