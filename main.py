import tkinter as tk
from tkinter import messagebox, ttk, Menu
from calibration import Calibration
from eye_tracker import EyeTracker
from blink_detector import BlinkDetector
from accessibility import Accessibility
from utils.tray_icon import TrayIcon
from utils.test_runner import TestRunner  # Import TestRunner
from utils.camera_manager import CameraDeviceManager
import keyboard
from pystray import Icon, Menu as SysMenu, MenuItem
from PIL import Image
import threading
import os


class EyeTrackingApp:
    """Main application to integrate all modules."""

    def __init__(self):
        self.eye_tracker = EyeTracker()
        self.blink_detector = BlinkDetector()
        self.accessibility = Accessibility()
        self.is_tracking = False
        self.tray_icon = None
        self.tracking_thread = None
        self.quit_to_tray = None
        self.selected_device = None

    def start_tracking(self):
        """Start eye tracking."""
        if not self.is_tracking:
            try:
                self.is_tracking = True
                device_index = int(self.selected_device.get().split("Index ")[1].rstrip(")"))
                self.accessibility.speak("Starting eye tracking.")
                print(f"Starting Eye Tracking on {self.selected_device.get()}...")
                self.tracking_thread = threading.Thread(target=self.eye_tracker.run, args=(device_index,), daemon=True)
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
        os._exit(0)  # Forcefully exit the program

    def create_tray_icon(self, root):
        """Create a system tray icon for the application."""
        icon_image = TrayIcon.load_tray_icon()

        # Define system tray menu options
        menu = SysMenu(
            MenuItem("Show Window", lambda: self.show_window(root)),
            MenuItem("Start Tracking", self.start_tracking),
            MenuItem("Stop Tracking", self.stop_tracking),
            MenuItem("Quit", self.quit_app)
        )

        # Initialize the tray icon
        self.tray_icon = Icon("EyeTracker", icon_image, "Eye Tracking Control", menu)

        # Left-click behavior: Restore the main window
        def on_left_click(icon, item=None):
            """Restore the main window when the tray icon is left-clicked."""
            root.after(0, lambda: self.show_window(root))  # Thread-safe call to deiconify

        # Use pystray's `icon.run_detached` and override the click behavior
        threading.Thread(target=lambda: self.tray_icon.run_detached(), daemon=True).start()

        # Attach the left-click event manually using the tray icon's notify handler
        self.tray_icon.notify = on_left_click


    def show_window(self, root):
        """Restore the main application window."""
        if root.state() == "withdrawn":
            root.deiconify()
            self.accessibility.speak("Window restored.")
            print("Window restored from system tray.")

    def run_tray_icon(self, root):
        """Run the tray icon in a separate thread."""
        threading.Thread(target=self.create_tray_icon, args=(root,), daemon=True).start()


def list_camera_devices():
    """List available camera devices with their friendly names."""
    devices = CameraDeviceManager.get_camera_devices()
    if devices:
        return CameraDeviceManager.format_devices(devices)
    return ["No cameras detected"]


def setup_shortcuts(app):
    """Set up keyboard shortcuts for the application."""
    keyboard.add_hotkey("ctrl+alt+t", lambda: app.start_tracking())
    keyboard.add_hotkey("ctrl+alt+b", lambda: app.start_blink_detection())
    keyboard.add_hotkey("ctrl+alt+c", lambda: app.show_calibration())
    keyboard.add_hotkey("ctrl+alt+s", lambda: app.stop_tracking())
    print("Keyboard shortcuts activated. Press Ctrl+Alt+T to start tracking.")


def setup_gui(app):
    """Setup the main application window."""
    root = tk.Tk()
    root.title("Eye Tracking Cursor Control")

    # Initialize variables
    app.quit_to_tray = tk.BooleanVar(value=True)
    app.selected_device = tk.StringVar(value="0")

    # Test output widget
    output_frame = tk.Frame(root)
    output_frame.pack(side=tk.BOTTOM, fill="both", expand=True, padx=10, pady=10)
    output_log = tk.Text(output_frame, wrap="word", height=10, state="disabled")
    output_log.pack(side=tk.LEFT, fill="both", expand=True)
    scroll_bar = tk.Scrollbar(output_frame, command=output_log.yview)
    scroll_bar.pack(side=tk.RIGHT, fill="y")
    output_log.config(yscrollcommand=scroll_bar.set)

    # Initialize TestRunner
    test_runner = TestRunner(output_widget=output_log)

    # Menu bar
    menu_bar = tk.Menu(root)

    # Tests Dropdown Menu
    tests_menu = tk.Menu(menu_bar, tearoff=0)
    for test_file in test_runner.tests:
        tests_menu.add_command(label=test_file, command=lambda t=test_file: test_runner.run_test(t))
    menu_bar.add_cascade(label="Tests", menu=tests_menu)

    root.config(menu=menu_bar)

    # Camera device selection
    tk.Label(root, text="Select Camera Device:").pack(pady=5)
    devices = list_camera_devices()
    device_selector = ttk.Combobox(root, textvariable=app.selected_device, state="readonly")
    device_selector["values"] = devices
    device_selector.set(devices[0])
    device_selector.pack(pady=5)

    # Main buttons
    tk.Button(root, text="Start Eye Tracking", command=app.start_tracking).pack(pady=10)
    tk.Button(root, text="Start Blink Detection", command=app.start_blink_detection).pack(pady=10)
    tk.Button(root, text="Calibrate", command=app.show_calibration).pack(pady=10)
    tk.Button(root, text="Stop Tracking", command=app.stop_tracking).pack(pady=10)

    # Quit behavior
    quit_frame = tk.Frame(root)
    tk.Checkbutton(quit_frame, text="Quit to Tray", variable=app.quit_to_tray).pack(side=tk.LEFT, padx=5)
    tk.Label(quit_frame, text="(Uncheck to quit completely)").pack(side=tk.LEFT, padx=5)
    quit_frame.pack(pady=10)

    def on_closing():
        if app.quit_to_tray.get():
            app.accessibility.speak("Minimizing to tray.")
            root.withdraw()
            threading.Thread(target=lambda: app.run_tray_icon(root), daemon=True).start()
        else:
            app.quit_app()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    app = EyeTrackingApp()
    setup_shortcuts(app)
    setup_gui(app)
