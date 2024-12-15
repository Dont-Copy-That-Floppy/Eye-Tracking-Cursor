# test_calibration.py
import unittest
import os
from calibration import Calibration


class TestCalibration(unittest.TestCase):
    """Unit tests for the Calibration module."""

    def setUp(self):
        """Set up test data and environment."""
        self.screen_points = [(100, 100), (200, 100), (300, 100)]
        self.detected_points = [(110, 105), (210, 95), (290, 110)]
        self.monitor_name = "TestMonitor"

    def tearDown(self):
        """Clean up any generated files."""
        matrix_path = f"calibration_data/homography_matrix_{self.monitor_name}.npy"
        if os.path.exists(matrix_path):
            os.remove(matrix_path)

    def test_map_gaze_to_screen(self):
        """Test that the homography matrix is saved correctly."""
        Calibration.map_gaze_to_screen(self.screen_points, self.detected_points, self.monitor_name)
        matrix_path = f"calibration_data/homography_matrix_{self.monitor_name}.npy"
        self.assertTrue(os.path.exists(matrix_path))

    def test_transform_gaze_to_screen(self):
        """Test gaze transformation using the saved homography matrix."""
        Calibration.map_gaze_to_screen(self.screen_points, self.detected_points, self.monitor_name)
        transformed_point = Calibration.transform_gaze_to_screen((110, 105), self.monitor_name)
        self.assertIsInstance(transformed_point, (tuple, list))
        self.assertEqual(len(transformed_point), 2)  # Ensure it's a 2D coordinate


if __name__ == "__main__":
    unittest.main()
