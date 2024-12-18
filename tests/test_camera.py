import unittest
import cv2
import os
import sys

# Fix the import path to ensure 'utils' is discoverable
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from utils.camera_manager import CameraDeviceManager  # Now import works correctly


class TestCameraManager(unittest.TestCase):
    """Unit tests for CameraDeviceManager."""

    def test_camera_device_detection(self):
        """Test that camera devices are detected."""
        devices = CameraDeviceManager.get_camera_devices()
        print("\nDetected Camera Devices:")
        for device in devices:
            print(f"Index: {device['index']}, Name: {device['name']}")
        self.assertIsInstance(devices, list, "Device list should be a list.")
        self.assertGreaterEqual(len(devices), 0, "Device list should not be negative.")

    def test_camera_accessibility(self):
        """Test that detected camera devices can be accessed."""
        devices = CameraDeviceManager.get_camera_devices()
        if not devices:
            self.skipTest("No cameras detected. Skipping accessibility test.")

        for device in devices:
            with self.subTest(device=device):
                print(f"Testing access for device: {device['name']} (Index {device['index']})")
                cap = cv2.VideoCapture(device["index"], cv2.CAP_DSHOW)
                self.assertTrue(cap.isOpened(), f"Camera '{device['name']}' (Index {device['index']}) should be accessible.")
                cap.release()

    def test_no_duplicate_devices(self):
        """Test that no duplicate camera devices are returned."""
        devices = CameraDeviceManager.get_camera_devices()
        device_indices = [device["index"] for device in devices]
        self.assertEqual(len(device_indices), len(set(device_indices)), "Device indices should not have duplicates.")


if __name__ == "__main__":
    unittest.main()
