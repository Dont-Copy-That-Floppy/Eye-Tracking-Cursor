import cv2
import numpy as np
from screeninfo import get_monitors
import os


class Calibration:
    """Handles calibration for accurate gaze tracking with multi-monitor support."""

    @staticmethod
    def run_calibration():
        """Runs the calibration process for all monitors."""
        monitors = get_monitors()  # Get information about all connected monitors
        calibration_data = {}

        for monitor in monitors:
            screen_width = monitor.width
            screen_height = monitor.height
            print(f"Calibrating for monitor: {monitor.name} ({screen_width}x{screen_height})")

            # Define a 3x3 grid for calibration points
            grid_points = [
                (screen_width // 4, screen_height // 4),  # Top-left
                (screen_width // 2, screen_height // 4),  # Top-center
                (3 * screen_width // 4, screen_height // 4),  # Top-right
                (screen_width // 4, screen_height // 2),  # Center-left
                (screen_width // 2, screen_height // 2),  # Center
                (3 * screen_width // 4, screen_height // 2),  # Center-right
                (screen_width // 4, 3 * screen_height // 4),  # Bottom-left
                (screen_width // 2, 3 * screen_height // 4),  # Bottom-center
                (3 * screen_width // 4, 3 * screen_height // 4),  # Bottom-right
            ]

            detected_points = []
            for point in grid_points:
                # Show calibration marker
                marker_frame = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
                cv2.circle(marker_frame, point, 30, (0, 255, 0), -1)
                cv2.imshow("Calibration", marker_frame)

                # Mock gaze detection: Replace this with gaze capturing logic
                key = cv2.waitKey(3000)  # Display marker for 3 seconds
                if key == 27:  # Exit on Esc
                    break
                # For real-world integration, replace the below line with gaze detection
                detected_points.append(point)

            cv2.destroyWindow("Calibration")

            if len(detected_points) == len(grid_points):
                Calibration.map_gaze_to_screen(grid_points, detected_points, monitor.name)
                calibration_data[monitor.name] = detected_points
            else:
                print(f"Calibration for monitor {monitor.name} was incomplete.")

        print("Calibration complete for all monitors.")
        return calibration_data

    @staticmethod
    def map_gaze_to_screen(screen_points, detected_gaze_points, monitor_name):
        """Maps detected gaze points to screen coordinates using homography."""
        try:
            screen_points = np.array(screen_points, dtype=np.float32)
            detected_gaze_points = np.array(detected_gaze_points, dtype=np.float32)
            homography_matrix, _ = cv2.findHomography(detected_gaze_points, screen_points)

            # Save the homography matrix for this monitor
            homography_dir = "calibration_data"
            os.makedirs(homography_dir, exist_ok=True)
            matrix_path = os.path.join(homography_dir, f"homography_matrix_{monitor_name}.npy")
            np.save(matrix_path, homography_matrix)
            print(f"Homography matrix saved for monitor: {monitor_name} at {matrix_path}")
        except Exception as e:
            print(f"Error mapping gaze to screen for monitor {monitor_name}: {e}")

    @staticmethod
    def transform_gaze_to_screen(gaze_point, monitor_name):
        """Transforms a gaze point using the saved homography matrix for the given monitor."""
        try:
            homography_dir = "calibration_data"
            matrix_path = os.path.join(homography_dir, f"homography_matrix_{monitor_name}.npy")
            if not os.path.exists(matrix_path):
                raise FileNotFoundError(f"Homography matrix for monitor {monitor_name} not found.")

            homography_matrix = np.load(matrix_path)
            gaze_point = np.array([[gaze_point]], dtype=np.float32)
            transformed_point = cv2.perspectiveTransform(gaze_point, homography_matrix)
            return transformed_point[0][0]
        except Exception as e:
            print(f"Error transforming gaze point for monitor {monitor_name}: {e}")
            return gaze_point  # Fallback to raw gaze point if transformation fails
