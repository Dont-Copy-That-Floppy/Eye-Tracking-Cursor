import cv2
import numpy as np
import os
from screeninfo import get_monitors
from utils.homography import HomographyManager
from eye_tracker import EyeTracker  # Import EyeTracker for gaze input
import time


class Calibration:
    """Handles calibration for accurate gaze tracking."""

    @staticmethod
    def run_calibration():
        """Runs the calibration process."""
        # Setup screen dimensions
        monitor = get_monitors()[0]
        window_width, window_height = monitor.width // 2, monitor.height // 2
        cv2.namedWindow("Calibration", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Calibration", window_width, window_height)
        cv2.moveWindow("Calibration", monitor.width // 4, monitor.height // 4)

        # Calibration grid points
        grid_points = [
            (window_width // 4, window_height // 4),
            (window_width // 2, window_height // 4),
            (3 * window_width // 4, window_height // 4),
            (window_width // 4, window_height // 2),
            (window_width // 2, window_height // 2),
            (3 * window_width // 4, window_height // 2),
            (window_width // 4, 3 * window_height // 4),
            (window_width // 2, 3 * window_height // 4),
            (3 * window_width // 4, 3 * window_height // 4),
        ]

        detected_gaze_points = []
        eye_tracker = EyeTracker()  # Initialize EyeTracker for real gaze input
        cap = cv2.VideoCapture(0)  # Start webcam capture

        if not cap.isOpened():
            print("Error: Camera not accessible for calibration.")
            return

        print("Follow the green dots with your eyes. Press SPACE to capture, or wait 2 seconds.")

        # Iterate through each calibration point
        for i, point in enumerate(grid_points):
            frame = np.zeros((window_height, window_width, 3), dtype=np.uint8)
            cv2.circle(frame, point, 20, (0, 255, 0), -1)
            cv2.putText(frame, f"Look at the dot ({i+1}/{len(grid_points)}).", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.imshow("Calibration", frame)

            # Initialize gaze position capture
            start_time = time.time()
            gaze_x, gaze_y = 0, 0
            gaze_samples = []

            while time.time() - start_time < 2:  # Capture gaze for 2 seconds
                ret, camera_frame = cap.read()
                if not ret:
                    continue
                gray = cv2.cvtColor(camera_frame, cv2.COLOR_BGR2GRAY)

                # Get gaze position
                gaze_position = eye_tracker.calculate_gaze_position(gray)
                if gaze_position:
                    gaze_samples.append(gaze_position)

                if cv2.waitKey(1) & 0xFF == ord(" "):  # Press SPACE to confirm point
                    break

            # Average the gaze samples for stability
            if gaze_samples:
                avg_gaze = np.mean(gaze_samples, axis=0)
                detected_gaze_points.append(avg_gaze)
                print(f"Captured gaze point {i + 1}: {avg_gaze}")
            else:
                print(f"Failed to capture gaze for point {i + 1}. Using fallback center point.")
                detected_gaze_points.append(point)  # Fallback to grid point

        cap.release()
        cv2.destroyWindow("Calibration")

        # Save homography matrix
        if len(detected_gaze_points) >= 4:
            HomographyManager.save_homography_matrix(grid_points, detected_gaze_points)
            print("Calibration complete.")
        else:
            print("Error: Not enough valid points for homography calculation.")

    @staticmethod
    def map_gaze_to_screen(gaze_point):
        """Transforms a gaze point using the saved homography matrix."""
        return HomographyManager.apply_homography(*gaze_point)
