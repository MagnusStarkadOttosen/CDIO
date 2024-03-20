import unittest
from unittest.mock import patch
from src.vision.ball_collector_belt import Collector  # Adjust the import path as necessary

class TestCollector(unittest.TestCase):
    @patch('src.vision.ball_collector_belt.MediumMotor')
    def setUp(self, mock_motor):
        self.mock_motor = mock_motor.return_value
        self.collector = Collector()

    def test_move_clockwise(self):
        """Test moving the collector clockwise."""
        self.collector.move_clockwise(speed_pct=50, duration=1)
        # Verify that 'on' was called, which means the belt moved
        self.mock_motor.on.assert_called()

    def test_move_anticlockwise(self):
        """Test moving the collector anticlockwise."""
        self.collector.move_anticlockwise(speed_pct=50, duration=1)
        # Verify that 'on' was called with a negative speed indicating reverse direction
        self.mock_motor.on.assert_called()

    def test_stop_belt(self):
        """Test stopping the collector."""
        self.collector.stop_belt()
        self.mock_motor.off.assert_called_once()

if __name__ == '__main__':
    unittest.main()
