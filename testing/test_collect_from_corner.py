import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import cv2
import sys
import os

from src.client.pc_client import ClientPC
from src.client.vision.shape_detection import detect_balls
from src.client.field.navigate_to_target import navigate_to_target
from src.client.vision.camera import capture_image, initialize_camera, close_camera
from src.client.field.coordinate_system import find_corner_points_full, warp_perspective
from src.client.field.collect_from_corner import collect_from_corner, robot_action_based_on_corners, get_ball_coordinates, check_corners
from testing.visualization import draw_circles

# Mock the ClientPC class
class MockClientPC:
    def send_command(self, command):
        print(f"Mock command sent: {command}")

def mock_initialize_camera(index):
    print(f"Mock camera initialized at index {index}")
    return "mock_camera"

def mock_capture_image(camera, filename):
    print(f"Mock image captured with camera {camera} and saved as {filename}")
    # Create a mock image for testing
    mock_image = cv2.imread('originalImages/newCourse.jpg')
    cv2.circle(mock_image, (300, 300), 50, (255, 255, 255), -1)  # Add a mock ball
    cv2.imwrite(f"images/capturedImage/{filename}", mock_image)

def mock_find_corner_points_full(image):
    print("Mock find corner points")
    return [(0, 0), (1800, 0), (0, 1200), (1800, 1200)]

def mock_warp_perspective(image, corners, dst_size):
    print("Mock warp perspective")
    return image

def mock_detect_robot(image):
    print("Mock detect robot")
    return (300, 300), 0  # Mock robot position and direction

class TestCollectFromCorner(unittest.TestCase):

    @patch('src.client.pc_client.ClientPC', new_callable=lambda: MockClientPC)
    @patch('src.client.vision.camera.initialize_camera', new_callable=lambda: mock_initialize_camera)
    @patch('src.client.vision.camera.capture_image', new_callable=lambda: mock_capture_image)
    @patch('src.client.field.coordinate_system.find_corner_points_full', new_callable=lambda: mock_find_corner_points_full)
    @patch('src.client.field.coordinate_system.warp_perspective', new_callable=lambda: mock_warp_perspective)
    @patch('src.client.vision.shape_detection.detect_robot', new_callable=lambda: mock_detect_robot)
    def test_collect_from_corner(self, mock_client_pc, mock_camera, mock_capture_image, mock_find_corners, mock_warp, mock_detect_robot):
        CORNERS = [(0, 0), (0, 1200), (1800, 0), (1800, 1200)]
        PIVOT_POINTS = [(300, 600), (1500, 600)]
        IMAGE_SIZE = [1200, 1800]

        client_pc = MockClientPC()
        camera = mock_initialize_camera(index=2)

        corner_point = (0, 0)
        collect_from_corner(client_pc, camera, corner_point)

if __name__ == '__main__':
    unittest.main()
