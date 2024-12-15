import cv2
import dlib
import time
from scipy.spatial import distance
import pyautogui


class BlinkDetector:
    """Detects blinks and allows sensitivity adjustments."""

    def __init__(self, blink_threshold=0.25, blink_duration=0.2, double_blink_interval=0.5):
        # Load pre-trained models
        self.detector = dlib.get_frontal_face_detector()
        # self.predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")  # Ensure model file is available
        self.predictor = dlib.shape_predictor("models/shape_predictor_5_face_landmarks.dat")

        # Eye landmark indices
        self.left_eye_indices = [36, 37, 38, 39, 40, 41]
        self.right_eye_indices = [42, 43, 44, 45, 46, 47]

        # Blink detection parameters
        self.blink_threshold = blink_threshold
        self.blink_duration = blink_duration
        self.double_blink_interval = double_blink_interval

        # State variables
        self.last_blink_time = 0
        self.blink_start_time = 0
        self.is_blinking = False

    def set_sensitivity(self, blink_threshold=None, blink_duration=None, double_blink_interval=None):
        """Adjust sensitivity parameters."""
        if blink_threshold:
            self.blink_threshold = blink_threshold
        if blink_duration:
            self.blink_duration = blink_duration
        if double_blink_interval:
            self.double_blink_interval = double_blink_interval

    def eye_aspect_ratio(self, eye_points):
        """Calculates the Eye Aspect Ratio (EAR) for an eye."""
        vertical_1 = distance.euclidean(eye_points[1], eye_points[5])
        vertical_2 = distance.euclidean(eye_points[2], eye_points[4])
        horizontal = distance.euclidean(eye_points[0], eye_points[3])
        ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
        return ear

    def detect_blinks(self, landmarks):
        """Calculates EAR and checks for blink status."""
        left_eye = [(landmarks.part(i).x, landmarks.part(i).y) for i in self.left_eye_indices]
        right_eye = [(landmarks.part(i).x, landmarks.part(i).y) for i in self.right_eye_indices]

        left_ear = self.eye_aspect_ratio(left_eye)
        right_ear = self.eye_aspect_ratio(right_eye)

        # Average EAR for both eyes
        avg_ear = (left_ear + right_ear) / 2.0
        return avg_ear

    def process_blink(self, blink_duration):
        """Handles blink actions based on blink duration."""
        if blink_duration < self.blink_duration:
            self.process_single_blink()
        elif self.blink_duration <= blink_duration < 2.0:  # Long blink threshold
            self.process_double_blink()
        else:
            self.process_long_blink()

    def process_single_blink(self):
        """Handles a single blink (e.g., left-click)."""
        print("Single Blink Detected: Left Click")
        pyautogui.click()

    def process_double_blink(self):
        """Handles a double blink (e.g., right-click)."""
        print("Double Blink Detected: Right Click")
        pyautogui.rightClick()

    def process_long_blink(self):
        """Handles a long blink (e.g., drag-and-drop)."""
        print("Long Blink Detected: Drag-and-Drop")
        pyautogui.mouseDown()
        time.sleep(0.5)  # Simulate dragging
        pyautogui.mouseUp()

    def run(self):
        """Runs the blink detection loop."""
        cap = cv2.VideoCapture(0)  # Start webcam capture
        if not cap.isOpened():
            print("Error: Webcam not accessible.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces
            faces = self.detector(gray)
            for face in faces:
                # Predict facial landmarks
                landmarks = self.predictor(gray, face)

                # Detect blinks
                ear = self.detect_blinks(landmarks)

                # Check EAR threshold for blink detection
                if ear < self.blink_threshold:  # Eye closed
                    if not self.is_blinking:
                        self.is_blinking = True
                        self.blink_start_time = time.time()
                else:  # Eye open
                    if self.is_blinking:
                        self.is_blinking = False
                        blink_duration = time.time() - self.blink_start_time
                        self.process_blink(blink_duration)

            # Display the frame for debugging
            cv2.putText(frame, f"Blink Threshold: {self.blink_threshold}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Blink Detector", frame)

            # Break loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
