import unittest
import cv2

from src.client.vision.shape_detection import detect_obstacles


class TestObstacleDetection(unittest.TestCase):

    def test_detect_obstacles(self):
        # Load test image
        test_image = cv2.imread('path_to_test_image.jpg')
        self.assertIsNotNone(test_image, "Failed to load test image.")

        # Call the function
        intersections = detect_obstacles(test_image)
        
        # Check if the result is as expected
        expected_number_of_intersections = 5  # Adjust based on known test image
        self.assertEqual(len(intersections), expected_number_of_intersections, "Number of intersections does not match.")

if __name__ == '__main__':
    unittest.main()
