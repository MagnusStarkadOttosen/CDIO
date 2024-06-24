import cv2
import unittest
from src.client.vision.pathfinder import *
from src.client.vision.shape_detection import detect_balls, detect_robot
from src.client.vision.filters import filter_image_white

class BallsRemainingTest(unittest.TestCase):

    def test_nearest_ball_coordinates(self):
        input_folder_path = 'images/'
        image_name = 'gen_warped2_newCourse_bigDots.jpg'
        input_image_path = input_folder_path + image_name
        image = cv2.imread(input_image_path)

        balls = detect_balls(filter_image_white(image))
        robot_pos, robot_direction = detect_robot(image)
        nearest = find_nearest_ball(robot_pos, balls)
        print(f"nearest x: {nearest[0]}, nearest y: {nearest[1]}")

    def test_are_balls_remaining(self):
        input_folder_path = 'images/'
        image_name = 'white_balls.jpeg'
        input_image_path = input_folder_path + image_name
        image = cv2.imread(input_image_path)

        balls = detect_balls(filter_image_white(image))

        expected = True
        actual = balls_are_remaining(balls)  # Assuming balls_are_remaining is defined somewhere
        self.assertEqual(expected, actual)


    def test_nearest_ball(self):
        input_folder_path = 'images/'
        image_name = '1.jpg'
        input_image_path = input_folder_path + image_name
        image = cv2.imread(input_image_path)


        shape_detector = Shapes(image)
        shape_detector.detect_balls()



        result = findNearestBall(np.array([0,0]),shape_detector)

        print("test 2",result.y)




        self.assertEqual(result.x, 1570)  # Expected x coordinate
        self.assertEqual(result.y, 1620)



if __name__ == '__main__':
    unittest.main()
