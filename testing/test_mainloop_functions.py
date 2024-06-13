from src.client.field.coordinate_system import warp_perspective
from src.client.hsvLoad import read_hsv_values
from src.client.pathfinding.GenerateNavMesh import GenerateNavMesh, astar, cells_to_coordinates, coordinate_to_cell, \
    optimize_path, find_path
from src.mainloop import MainLoop
from src.client.vision.shape_detection import detect_robot

WHITE_BALL_COUNT = 10
ROBOT_CAPACITY = 6
TOLERANCE = 10
TURN_SPEED = 3
DST_SIZE = (1200, 1800)
PIVOT_POINTS = [(300, 600), (1500, 600)]
CORNERS = {
    "top_left": (0, 0),
    "bottom_left": (0, 1200),
    "top_right": (1800, 0),
    "bottom_right": (1800, 1200)
}


def test_nav_to_target_hardcoded_path(ml):
    path = [(300, 600), (1500, 600)]
    ml.target_pos = (100,600)
    ml._navigate_to_target(path)


def pretty_print_navmesh(navmesh, path):
    navmesh_copy = navmesh.copy()
    for (x, y) in path:
        navmesh_copy[y, x] = 2  # Mark the path with '2'

    for row in navmesh_copy:
        print(' '.join(str(cell) for cell in row))


def test_nav_to_target_detected_path(ml):
    ret, frame = ml.camera.read()
    warped_img = warp_perspective(frame, ml.final_points, DST_SIZE)
    print(f"testing colors {ml.direction_color}")
    robot_pos, robot_direction = detect_robot(warped_img, ml.direction_color, ml.pivot_color)
    while robot_pos is None or robot_direction is None:
        robot_pos, robot_direction = detect_robot(warped_img, ml.direction_color, ml.pivot_color)

    print(f"robot_pos: {robot_pos}, robot_direction: {robot_direction}")
    # ml.target_pos = (ml.balls[0][0], ml.balls[0][1])
    # print(f"target_position: {ml.target_pos}")

    red_hsv_values = read_hsv_values('hsv_presets_red.txt')
    navmesh = GenerateNavMesh(warped_img, red_hsv_values)
    pretty_print_navmesh(navmesh, [])
    print("sdfdjsdjkjkdsfd")
    robotCell = coordinate_to_cell(robot_pos[0], robot_pos[1], 30)



    targetCell = coordinate_to_cell(400, 600, 30)
    print(f"robotCell: {robotCell}, targetCell: {targetCell}")
    print(f"x: {robotCell[0]}, y: {robotCell[1]}")
    print(f"asdasdas {navmesh[robotCell[1], robotCell[0]]}")

    path = astar(navmesh, robotCell, targetCell)
    # while path is None:
    #     print("try again")
    #     path = astar(navmesh, robotCell, targetCell)


    print(f"path {path}")
    optimized_path = optimize_path(navmesh, path)
    print(f"optimized path: {optimized_path}")

    coord_path = cells_to_coordinates(optimized_path, 30)

    print(f"coord_path: {coord_path}")

    ml._navigate_to_target(coord_path)


def test_nav_to_target_with_find_path(ml):
    ret, frame = ml.camera.read()
    warped_img = warp_perspective(frame, ml.final_points, DST_SIZE)
    print(f"testing colors {ml.direction_color}")
    robot_pos, robot_direction = detect_robot(warped_img, ml.direction_color, ml.pivot_color)
    while robot_pos is None or robot_direction is None:
        robot_pos, robot_direction = detect_robot(warped_img, ml.direction_color, ml.pivot_color)

    print(f"robot_pos: {robot_pos}, robot_direction: {robot_direction}")
    path = find_path()


def test_collect_nearest_ball(ml): # many white balls on field
    ml._collect_ball("filter_image_white")


main_loop = MainLoop()
main_loop.initialize_field()
# main_loop._detect_initial_balls()
# test_nav_to_target_hardcoded_path(main_loop)
test_nav_to_target_detected_path(main_loop)
# test_collect_nearest_ball(main_loop)

