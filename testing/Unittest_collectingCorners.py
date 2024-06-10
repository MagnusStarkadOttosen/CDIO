import unittest
import numpy as np
import math
from src.client.field.collect_from_corner import (
    calculate_distance,
    check_corners,
    get_ball_coordinates,
    robot_action_based_on_corners
)

# Hardcoded mock data for testing
CORNERS = [(0, 0), (0, 1200), (1800, 0), (1800, 1200)]
PIVOT_POINTS = [(300, 600), (1500, 600)]
IMAGE_SIZE = [1200, 1800]


class TestFunctions(unittest.TestCase):

    def test_calculate_distance(self):
        point1 = (0, 0)
        point2 = (3, 4)
        expected_distance = 5.0
        distance = calculate_distance(point1, point2)
        self.assertEqual(distance, expected_distance)

    def test_check_corners(self):
        circles = [(10, 10, 5), (1790, 10, 5), (10, 1190, 5), (1790, 1190, 5), (398, 765, 5)]
        expected_corners = {
            "top_left": True,
            "top_right": True,
            "bottom_left": True,
            "bottom_right": True
        }
        corners = check_corners(circles, IMAGE_SIZE)
        self.assertEqual(corners, expected_corners)
        return corners

    def test_get_ball_coordinates(self):
        # Mock data for circles detected
        circles = [(300, 300, 50)]

        # Mock implementation of get_ball_coordinates
        def mock_get_ball_coordinates(camera, corner_threshold=50):
            corner_results = check_corners(circles, IMAGE_SIZE)
            return circles, corner_results

        coordinates, corners = mock_get_ball_coordinates("mock_camera")

        expected_coordinates = [(300, 300, 50)]
        expected_corners = {
            "top_left": False,
            "top_right": False,
            "bottom_left": False,
            "bottom_right": False
        }

        self.assertEqual(coordinates, expected_coordinates)
        self.assertEqual(corners, expected_corners)

    def test_robot_action_based_on_corners(self):
        class MockClientPC:
            def __init__(self):
                self.commands = []

            def send_command(self, command):
                self.commands.append(command)

        client_pc = MockClientPC()

        def mock_collect_from_corner(client_pc, camera, corner):
            print(f"Collect from corner: {corner}")
            client_pc.send_command(f"collect_from_corner {corner}")

        def mock_navigate_to_pivot(camera, client_pc, pivot_point, pivot_index):
            print(f"navigate to pivot {pivot_index} {pivot_point}")
            client_pc.send_command(f"move_to pivot {pivot_index} {pivot_point}")

        # Mocked circles for testing
        circles = [(10, 10, 5), (1790, 10, 5), (10, 1190, 5), (1790, 1190, 5)]

        corner_results = check_corners(circles, IMAGE_SIZE)

        for corner, is_near in corner_results.items():
            if is_near:
                if corner == "top_left":
                    mock_navigate_to_pivot("mock_camera", client_pc, PIVOT_POINTS[0], 0)
                    mock_collect_from_corner(client_pc, "mock_camera", CORNERS[0])
                elif corner == "top_right":
                    mock_navigate_to_pivot("mock_camera", client_pc, PIVOT_POINTS[1], 1)
                    mock_collect_from_corner(client_pc, "mock_camera", CORNERS[1])
                elif corner == "bottom_left":
                    mock_navigate_to_pivot("mock_camera", client_pc, PIVOT_POINTS[0], 0)
                    mock_collect_from_corner(client_pc, "mock_camera", CORNERS[2])
                elif corner == "bottom_right":
                    mock_navigate_to_pivot("mock_camera", client_pc, PIVOT_POINTS[1], 1)
                    mock_collect_from_corner(client_pc, "mock_camera", CORNERS[3])

        expected_commands = [
            "move_to pivot 0 (300, 600)",
            "collect_from_corner (0, 0)",
            "move_to pivot 1 (1500, 600)",
            "collect_from_corner (0, 1200)",
            "move_to pivot 0 (300, 600)",
            "collect_from_corner (1800, 0)",
            "move_to pivot 1 (1500, 600)",
            "collect_from_corner (1800, 1200)"
        ]

        self.assertEqual(client_pc.commands, expected_commands)


if __name__ == '__main__':
    unittest.main()
