import tkinter as tk
from tkinter import messagebox
from calibration import Calibration
from eye_tracker import EyeTracker
from blink_detector import BlinkDetector
from accessibility import Accessibility
from utils.tray_icon import TrayIcon  # Import TrayIcon utility for tray icon loading
import keyboard
from pystray import Icon, Menu, MenuItem
import threading


class EyeTrackingApp:
    """Main application to integrate all modules."""

    def __init__(self):
        self.eye_tracker = EyeTracker()
        self.blink_detector = BlinkDetector()
        self.accessibility = Accessibility()
        self.is_tracking = False
        self.tray_icon = None
        self.tracking_thread = None

    def start_tracking(self):
        """Start eye tracking."""
        if not self.is_tracking:
            try:
                self.is_tracking = True
                self.accessibility.speak("Starting eye tracking.")
                print("Starting Eye Tracking...")
                self.tracking_thread = threading.Thread(target=self.eye_tracker.run, daemon=True)
                self.tracking_thread.start()
            except Exception as e:
                self.accessibility.speak("Error occurred while starting eye tracking.")
                messagebox.showerror("Error", f"An error occurred: {e}")

    def start_blink_detection(self):
        """Start blink detection."""
        try:
            self.accessibility.speak("Starting blink detection.")
            print("Starting Blink Detection...")
            self.blink_detector.run()
        except Exception as e:
            self.accessibility.speak("Error occurred while starting blink detection.")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_calibration(self):
        """Run the calibration module."""
        try:
            self.accessibility.speak("Starting calibration.")
            print("Running Calibration...")
            Calibration.run_calibration()
        except Exception as e:
            self.accessibility.speak("Calibration failed.")
            messagebox.showerror("Error", f"Calibration failed: {e}")

    def stop_tracking(self):
        """Stop the tracking system gracefully."""
        if self.is_tracking:
            self.is_tracking = False
            self.accessibility.speak("Stopping tracking.")
            print("Tracking stopped.")
            messagebox.showinfo("Info", "Tracking stopped.")

    def quit_app(self):
        """Quit the application."""
        self.stop_tracking()
        if self.tray_icon:
            self.tray_icon.stop()
        print("Application exited.")

    def create_tray_icon(self):
        """Create a system tray icon for the application."""
        # Use TrayIcon utility to load and resize the tray icon
        icon_image = TrayIcon.load_tray_icon()

        # Define menu options
        menu = Menu(MenuItem("Start Tracking", self.start_tracking), MenuItem("Stop Tracking", self.stop_tracking), MenuItem("Quit", self.quit_app))

        # Initialize the tray icon
        self.tray_icon = Icon("EyeTracker", icon_image, "Eye Tracking Control", menu)

    def run_tray_icon(self):
        """Run the tray icon in a separate thread."""
        self.create_tray_icon()
        self.tray_icon.run()


def setup_shortcuts(app):
    """Set up keyboard shortcuts for the application."""
    keyboard.add_hotkey("ctrl+alt+t", lambda: app.start_tracking())  # Start Tracking
    keyboard.add_hotkey("ctrl+alt+b", lambda: app.start_blink_detection())  # Start Blink Detection
    keyboard.add_hotkey("ctrl+alt+c", lambda: app.show_calibration())  # Start Calibration
    keyboard.add_hotkey("ctrl+alt+s", lambda: app.stop_tracking())  # Stop Tracking
    print("Keyboard shortcuts activated. Press Ctrl+Alt+T to start tracking.")


def setup_gui(app):
    """Setup the main application window."""
    root = tk.Tk()
    root.title("Eye Tracking Cursor Control")

    # Buttons for user interaction
    tk.Button(root, text="Start Eye Tracking", command=app.start_tracking).pack(pady=10)
    tk.Button(root, text="Start Blink Detection", command=app.start_blink_detection).pack(pady=10)
    tk.Button(root, text="Calibrate", command=app.show_calibration).pack(pady=10)
    tk.Button(root, text="Stop Tracking", command=app.stop_tracking).pack(pady=10)

    # Minimize to tray
    def on_closing():
        app.accessibility.speak("Minimizing to tray.")
        root.withdraw()
        threading.Thread(target=app.run_tray_icon, daemon=True).start()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    app = EyeTrackingApp()
    setup_shortcuts(app)
    setup_gui(app)  # Run the GUI
