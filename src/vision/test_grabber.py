import unittest
from unittest.mock import patch
from grabber import Grabber

class TestGrabber(unittest.TestCase):

    @patch('grabber.MediumMotor')
    def setUp(self, MockMotor):
        # Initialize a Grabber instance for testing
        self.grabber = Grabber()

    def test_open(self):
        """Test that the grabber can open without errors."""
        try:
            self.grabber.open()
        except Exception as e:
            self.fail(f"Open method failed with an exception {e}")

    def test_close(self):
        """Test that the grabber can close without errors."""
        try:
            self.grabber.close()
        except Exception as e:
            self.fail(f"Close method failed with an exception {e}")

    def test_hold(self):
        """Test that the grabber can hold a position without errors."""
        try:
            self.grabber.hold(90)  # Arbitrary position for testing
        except Exception as e:
            self.fail(f"Hold method failed with an exception {e}")

if __name__ == '__main__':
    unittest.main()
