from PIL import Image, ImageDraw
import os

class TrayIcon:
    """Handles tray icon image loading and resizing."""

    @staticmethod
    def load_tray_icon(icon_directory="assets/icons", default_size=(64, 64)):
        """
        Loads and resizes a tray icon (JPEG or PNG) from the specified directory.

        Args:
            icon_directory (str): The directory where tray icons are stored.
            default_size (tuple): The target size for the tray icon.

        Returns:
            Image: The resized tray icon.
        """
        # Supported extensions
        supported_extensions = [".png", ".jpg", ".jpeg"]

        # Search for an icon in the directory
        for file_name in os.listdir(icon_directory):
            if any(file_name.lower().endswith(ext) for ext in supported_extensions):
                icon_path = os.path.join(icon_directory, file_name)
                try:
                    # Open and resize the image
                    tray_icon = Image.open(icon_path).convert("RGBA")
                    tray_icon = tray_icon.resize(default_size, Image.ANTIALIAS)
                    print(f"Tray icon loaded: {icon_path}")
                    return tray_icon
                except Exception as e:
                    print(f"Error loading tray icon {icon_path}: {e}")

        # Fallback: Generate a blank icon if none is found
        print("No tray icon found. Generating a default blank icon.")
        blank_icon = Image.new("RGBA", default_size, (0, 0, 255))  # Blue background
        draw = ImageDraw.Draw(blank_icon)
        draw.ellipse((16, 16, 48, 48), fill=(255, 255, 255))  # Draw a white circle
        return blank_icon
