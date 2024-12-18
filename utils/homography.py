import os
import cv2
import numpy as np


class HomographyManager:
    """Handles saving, loading, and applying the homography matrix."""

    @staticmethod
    def save_homography_matrix(screen_points, gaze_points, file_path="calibration_data/homography_matrix.npy"):
        """Calculates and saves the homography matrix."""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            screen_points = np.array(screen_points, dtype=np.float32)
            gaze_points = np.array(gaze_points, dtype=np.float32)

            homography_matrix, _ = cv2.findHomography(gaze_points, screen_points)
            np.save(file_path, homography_matrix)
            print(f"Homography matrix saved to {file_path}")
        except Exception as e:
            print(f"Error saving homography matrix: {e}")

    @staticmethod
    def load_homography_matrix(file_path="calibration_data/homography_matrix.npy"):
        """Loads the homography matrix."""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError("Homography matrix not found. Run calibration first.")
            matrix = np.load(file_path)
            print("Homography matrix loaded successfully.")
            return matrix
        except Exception as e:
            print(f"Error loading homography matrix: {e}")
            return None

    @staticmethod
    def apply_homography(gaze_x, gaze_y, homography_matrix):
        """Applies the homography matrix to transform gaze coordinates."""
        try:
            gaze_point = np.array([[gaze_x, gaze_y]], dtype=np.float32).reshape(1, 1, 2)
            transformed_point = cv2.perspectiveTransform(gaze_point, homography_matrix)
            return transformed_point[0][0]
        except Exception as e:
            print(f"Error applying homography: {e}")
            return None, None
