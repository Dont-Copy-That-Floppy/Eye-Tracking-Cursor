import cv2
import dlib
import pyautogui
import numpy as np
from screeninfo import get_monitors


class EyeTracker:
    """Handles real-time eye tracking and cursor control."""

    def __init__(self):
        # Load pre-trained models
        self.detector = dlib.get_frontal_face_detector()
        # self.predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")  # Ensure model file is available
        self.predictor = dlib.shape_predictor("models/shape_predictor_5_face_landmarks.dat")

        # Initialize screen dimensions for multi-monitor setups
        self.monitors = get_monitors()
        self.screen_width = sum(monitor.width for monitor in self.monitors)
        self.screen_height = max(monitor.height for monitor in self.monitors)

        # State variables for active monitor detection
        self.active_monitor = self.monitors[0]

    def get_eye_region(self, landmarks, eye_indices):
        """Extracts the eye region from the facial landmarks."""
        return np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in eye_indices])

    def detect_active_monitor(self, gaze_x, gaze_y):
        """Detects which monitor the gaze is currently focused on."""
        for monitor in self.monitors:
            if monitor.x <= gaze_x <= monitor.x + monitor.width and monitor.y <= gaze_y <= monitor.y + monitor.height:
                self.active_monitor = monitor
                break

    def map_to_screen_coordinates(self, gaze_x, gaze_y, frame_width, frame_height):
        """Maps gaze coordinates to the active monitor's screen."""
        # Scale gaze to overall screen resolution
        scaled_x = int((gaze_x / frame_width) * self.screen_width)
        scaled_y = int((gaze_y / frame_height) * self.screen_height)

        # Detect and adjust for the active monitor
        self.detect_active_monitor(scaled_x, scaled_y)
        adjusted_x = scaled_x - self.active_monitor.x
        adjusted_y = scaled_y - self.active_monitor.y
        return adjusted_x, adjusted_y

    def calculate_gaze(self, eye_region):
        """Calculates the average position of the pupil in the eye region."""
        # Use the center of the eye region for simplicity (improve with pupil detection if needed)
        return np.mean(eye_region[:, 0]), np.mean(eye_region[:, 1])

    def run(self):
        """Runs the eye tracking loop."""
        cap = cv2.VideoCapture(0)  # Start webcam capture
        if not cap.isOpened():
            print("Error: Webcam not accessible.")
            return

        left_eye_indices = [36, 37, 38, 39, 40, 41]
        right_eye_indices = [42, 43, 44, 45, 46, 47]

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Convert frame to grayscale for detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the frame
            faces = self.detector(gray)
            for face in faces:
                # Predict facial landmarks
                landmarks = self.predictor(gray, face)

                # Extract eye regions
                left_eye = self.get_eye_region(landmarks, left_eye_indices)
                right_eye = self.get_eye_region(landmarks, right_eye_indices)

                # Calculate gaze positions for both eyes
                left_gaze_x, left_gaze_y = self.calculate_gaze(left_eye)
                right_gaze_x, right_gaze_y = self.calculate_gaze(right_eye)

                # Average gaze positions
                gaze_x = (left_gaze_x + right_gaze_x) / 2
                gaze_y = (left_gaze_y + right_gaze_y) / 2

                # Map gaze to screen coordinates
                cursor_x, cursor_y = self.map_to_screen_coordinates(gaze_x, gaze_y, frame.shape[1], frame.shape[0])

                # Move the cursor
                pyautogui.moveTo(cursor_x, cursor_y)

                # Visualize gaze regions and cursor position
                cv2.polylines(frame, [left_eye], True, (0, 255, 0), 1)
                cv2.polylines(frame, [right_eye], True, (0, 255, 0), 1)
                cv2.circle(frame, (int(gaze_x), int(gaze_y)), 5, (255, 0, 0), -1)
                cv2.putText(frame, f"Cursor: ({cursor_x}, {cursor_y})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Display the frame for debugging
            cv2.imshow("Eye Tracker", frame)

            # Break loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
