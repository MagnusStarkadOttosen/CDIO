import unittest
import math

def calculate_distance(corner_point, target_point):
    return math.sqrt((target_point[0] - corner_point[0]) ** 2 + (target_point[1] - corner_point[1]) ** 2)

class TestNavigationDistances(unittest.TestCase):

    def setUp(self):
        # Define some example pivot points and corners
        self.pivot_point_1 = (300, 600)
        self.pivot_point_2 = (1500, 600)
        self.corner_top_left = (0, 0)
        self.corner_bottom_left = (0, 1200)
        self.corner_top_right = (1800, 0)
        self.corner_bottom_right = (1800, 1200)

    def test_distance_to_top_left(self):
        result = calculate_distance(self.pivot_point_1, self.corner_top_left)
        expected = math.sqrt((300 - 0)**2 + (600 - 0)**2)
        print(f"Test to Top Left: Result={result}, Expected={expected}")
        self.assertAlmostEqual(result, expected)

    def test_distance_to_bottom_right(self):
        result = calculate_distance(self.pivot_point_2, self.corner_bottom_right)
        expected = math.sqrt((1500 - 1800)**2 + (600 - 1200)**2)
        print(f"Test to Bottom Right: Result={result}, Expected={expected}")
        self.assertAlmostEqual(result, expected)

    def test_distance_between_diagonal_corners(self):
        result = calculate_distance(self.corner_top_left, self.corner_bottom_right)
        expected = math.sqrt((0 - 1800)**2 + (0 - 1200)**2)
        print(f"Test between Diagonal Corners: Result={result}, Expected={expected}")
        self.assertAlmostEqual(result, expected)

    def test_distance_between_same_points(self):
        result = calculate_distance(self.pivot_point_1, self.pivot_point_1)
        print(f"Test between Same Points: Result={result}, Expected=0")
        self.assertEqual(result, 0)

    def test_distance_with_negative_coordinates(self):
        result = calculate_distance((-200, -300), (-400, -600))
        expected = math.sqrt((-200 + 400)**2 + (-300 + 600)**2)
        print(f"Test with Negative Coordinates: Result={result}, Expected={expected}")
        self.assertAlmostEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
