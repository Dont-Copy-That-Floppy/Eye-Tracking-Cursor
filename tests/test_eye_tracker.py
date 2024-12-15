# test_eye_tracker.py
import unittest
import numpy as np
from eye_tracker import EyeTracker


class TestEyeTracker(unittest.TestCase):
    """Unit tests for the EyeTracker module."""

    def setUp(self):
        """Set up test data."""
        self.eye_tracker = EyeTracker()
        self.landmarks = lambda: None
        self.landmarks.part = lambda i: lambda: None
        self.landmarks.part = lambda i: type("Point", (), {"x": i * 10, "y": i * 5})

    def test_get_eye_region(self):
        """Test extraction of eye regions."""
        left_eye_indices = [36, 37, 38, 39, 40, 41]
        right_eye_indices = [42, 43, 44, 45, 46, 47]
        left_eye, right_eye = self.eye_tracker.get_eye_region(self.landmarks, left_eye_indices, right_eye_indices)
        self.assertEqual(len(left_eye), len(left_eye_indices))
        self.assertEqual(len(right_eye), len(right_eye_indices))

    def test_map_to_screen_coordinates(self):
        """Test gaze-to-screen mapping."""
        screen_width, screen_height = 1920, 1080
        cursor_x, cursor_y = self.eye_tracker.map_to_screen_coordinates(500, 500, 640, 480)
        self.assertGreaterEqual(cursor_x, 0)
        self.assertGreaterEqual(cursor_y, 0)
        self.assertLessEqual(cursor_x, screen_width)
        self.assertLessEqual(cursor_y, screen_height)


if __name__ == "__main__":
    unittest.main()
