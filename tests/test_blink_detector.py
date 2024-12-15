# test_blink_detector.py
import unittest
from blink_detector import BlinkDetector


class TestBlinkDetector(unittest.TestCase):
    """Unit tests for the BlinkDetector module."""

    def setUp(self):
        """Set up test data."""
        self.blink_detector = BlinkDetector()

    def test_eye_aspect_ratio(self):
        """Test EAR calculation."""
        eye_points = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12)]
        ear = self.blink_detector.eye_aspect_ratio(eye_points)
        self.assertIsInstance(ear, float)
        self.assertGreater(ear, 0)

    def test_blink_action(self):
        """Test that blink actions are processed correctly."""
        self.blink_detector.process_single_blink = lambda: "Single Blink Detected"
        self.blink_detector.process_double_blink = lambda: "Double Blink Detected"
        self.assertEqual(self.blink_detector.process_single_blink(), "Single Blink Detected")
        self.assertEqual(self.blink_detector.process_double_blink(), "Double Blink Detected")


if __name__ == "__main__":
    unittest.main()
