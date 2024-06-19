import unittest

def adjust_target_position(original_position, scale_factor):
    """Adjusts the given position based on the provided scale factor."""
    adjusted_x = original_position[0] * scale_factor
    adjusted_y = original_position[1] * scale_factor
    return (adjusted_x, adjusted_y)

class TestCalculateCorrectedPosition(unittest.TestCase):
    def setUp(self):
        """Set up the test scenario environment."""
        self.scale_factor = (182 - 23) / 182  # Example scale_factor from camera height and robot height
        self.targets = {
            "top_left": (0, 0),
            "bottom_left": (0, 1200),
            "top_right": (1800, 0),
            "bottom_right": (1800, 1200)
        }
        self.expected_positions = {
            "top_left": (0.0, 0.0),
            "bottom_left": (0.0, 1200 * self.scale_factor),
            "top_right": (1800 * self.scale_factor, 0.0),
            "bottom_right": (1800 * self.scale_factor, 1200 * self.scale_factor)
        }

    def test_corrected_positions(self):
        """Test that the corrected positions are calculated correctly."""
        for corner, original_pos in self.targets.items():
            with self.subTest(corner=corner):
                adjusted_pos = adjust_target_position(original_pos, self.scale_factor)
                expected_pos = self.expected_positions[corner]
                self.assertAlmostEqual(adjusted_pos[0], expected_pos[0], places=2,
                                       msg=f"X-coordinate mismatch at {corner}")
                self.assertAlmostEqual(adjusted_pos[1], expected_pos[1], places=2,
                                       msg=f"Y-coordinate mismatch at {corner}")
                print(f"Testing {corner}: Calculated: {adjusted_pos}, Expected: {expected_pos}")

if __name__ == '__main__':
    unittest.main()
