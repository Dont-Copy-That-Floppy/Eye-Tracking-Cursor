# visualizer.py
import cv2
import numpy as np


class Visualizer:
    """Utilities for visualizing landmarks and debug information."""

    @staticmethod
    def draw_eye_region(frame, eye_region, color=(0, 255, 0)):
        """Draws the eye region on the frame."""
        cv2.polylines(frame, [np.array(eye_region, dtype=np.int32)], True, color, 1)

    @staticmethod
    def draw_gaze_point(frame, x, y, color=(255, 0, 0)):
        """Draws the gaze point on the frame."""
        cv2.circle(frame, (int(x), int(y)), 5, color, -1)

    @staticmethod
    def overlay_text(frame, text, position=(10, 30), color=(0, 255, 0)):
        """Overlays text on the frame."""
        cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
