import cv2
import dlib
import pyautogui
import numpy as np
from screeninfo import get_monitors
from utils.homography import HomographyManager


class EyeTracker:
    """Handles real-time eye tracking and cursor control."""

    def __init__(self):
        # Load pre-trained models
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("models/shape_predictor_5_face_landmarks.dat")

        # Initialize screen dimensions for multi-monitor setups
        self.monitors = get_monitors()
        self.screen_width = sum(monitor.width for monitor in self.monitors)
        self.screen_height = max(monitor.height for monitor in self.monitors)

        # State variables for active monitor detection
        self.active_monitor = self.monitors[0]

        # Load homography matrix from calibration
        self.homography_matrix = self.load_homography_matrix()

    def load_homography_matrix(self):
        """Loads the homography matrix saved during calibration."""
        try:
            matrix_path = "calibration_data/homography_matrix.npy"
            homography_matrix = np.load(matrix_path)
            print("Homography matrix loaded successfully.")
            return homography_matrix
        except FileNotFoundError:
            print("Homography matrix not found. Run calibration first.")
            return None

    def get_eye_region(self, landmarks, eye_indices):
        """Extracts the eye region from the facial landmarks."""
        try:
            if landmarks is None:
                raise ValueError("No landmarks detected.")
            eye_points = [(landmarks.part(i).x, landmarks.part(i).y) for i in eye_indices]
            return np.array(eye_points)
        except (IndexError, ValueError) as e:
            print(f"Error extracting eye region: {e}")
            return np.array([])

    def calculate_gaze_position(self, gray_frame):
        """Calculates the average gaze position."""
        faces = self.detector(gray_frame)
        for face in faces:
            landmarks = self.predictor(gray_frame, face)
            left_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in [36, 37, 38, 39, 40, 41]])
            right_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in [42, 43, 44, 45, 46, 47]])

            if left_eye.size and right_eye.size:
                gaze_x = (np.mean(left_eye[:, 0]) + np.mean(right_eye[:, 0])) / 2
                gaze_y = (np.mean(left_eye[:, 1]) + np.mean(right_eye[:, 1])) / 2
                return gaze_x, gaze_y
        return None

    def calculate_gaze(self, eye_region):
        """Calculates the average position of the pupil in the eye region."""
        if eye_region.size > 0:
            return np.mean(eye_region[:, 0]), np.mean(eye_region[:, 1])
        return None, None

    def map_gaze_to_screen(self, gaze_x, gaze_y):
        """Maps gaze coordinates to screen coordinates using the homography matrix."""
        try:
            if self.homography_matrix is None:
                raise ValueError("Homography matrix not loaded. Run calibration first.")
            gaze_point = np.array([[gaze_x, gaze_y]], dtype=np.float32).reshape(1, 1, 2)
            transformed_point = cv2.perspectiveTransform(gaze_point, self.homography_matrix)
            screen_x, screen_y = transformed_point[0][0]
            return int(screen_x), int(screen_y)
        except Exception as e:
            print(f"Error mapping gaze to screen: {e}")
            return None, None

    def run(self, device_index=0):
        """Runs the eye tracking loop."""
        cap = cv2.VideoCapture(device_index)  # Open selected camera
        if not cap.isOpened():
            print(f"Error: Camera device {device_index} not accessible.")
            return

        left_eye_indices = [36, 37, 38, 39, 40, 41]
        right_eye_indices = [42, 43, 44, 45, 46, 47]

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.detector(gray)
            for face in faces:
                # Predict facial landmarks
                landmarks = self.predictor(gray, face)

                # Extract and calculate gaze positions
                left_eye = self.get_eye_region(landmarks, left_eye_indices)
                right_eye = self.get_eye_region(landmarks, right_eye_indices)

                if left_eye.size == 0 or right_eye.size == 0:
                    print("Eye region not detected. Skipping frame.")
                    continue

                left_gaze_x, left_gaze_y = self.calculate_gaze(left_eye)
                right_gaze_x, right_gaze_y = self.calculate_gaze(right_eye)

                if None in (left_gaze_x, left_gaze_y, right_gaze_x, right_gaze_y):
                    continue

                # Average the gaze positions
                gaze_x = (left_gaze_x + right_gaze_x) / 2
                gaze_y = (left_gaze_y + right_gaze_y) / 2

                # Map gaze coordinates to screen
                screen_x, screen_y = self.map_gaze_to_screen(gaze_x, gaze_y)
                if screen_x is not None and screen_y is not None:
                    # Clamp the cursor position to the screen bounds
                    screen_x = min(max(0, screen_x), self.screen_width)
                    screen_y = min(max(0, screen_y), self.screen_height)
                    pyautogui.moveTo(screen_x, screen_y)

                # Visualize for debugging
                cv2.putText(frame, f"Gaze: ({gaze_x:.1f}, {gaze_y:.1f})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Screen: ({screen_x}, {screen_y})", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            cv2.imshow("Eye Tracker", frame)

            # Break loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
