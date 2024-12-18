from pygrabber.dshow_graph import FilterGraph


class CameraDeviceManager:
    """Manages camera device detection and retrieval of friendly names."""

    @staticmethod
    def get_camera_devices():
        """
        Retrieve available camera devices with their friendly names.

        Returns:
            list: A list of dictionaries containing 'index' and 'name'.
        """
        try:
            # Use pygrabber to get the list of input devices
            graph = FilterGraph()
            device_names = graph.get_input_devices()

            devices = [{"index": idx, "name": name} for idx, name in enumerate(device_names)]
            return devices
        except Exception as e:
            print(f"Error retrieving camera devices: {e}")
            return []

    @staticmethod
    def format_devices(devices):
        """
        Format devices into a user-friendly list.

        Args:
            devices (list): List of camera device dictionaries.

        Returns:
            list: Formatted list of device strings.
        """
        return [f"{device['name']} (Index {device['index']})" for device in devices]


# Example usage for testing:
if __name__ == "__main__":
    manager = CameraDeviceManager()
    devices = manager.get_camera_devices()
    if devices:
        print("Available Camera Devices:")
        for device in CameraDeviceManager.format_devices(devices):
            print(device)
    else:
        print("No camera devices found.")
