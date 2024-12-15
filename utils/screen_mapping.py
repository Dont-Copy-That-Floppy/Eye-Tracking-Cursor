# screen_mapping.py
from screeninfo import get_monitors


class ScreenMapping:
    """Handles screen coordinate mapping and monitor management."""

    def __init__(self):
        self.monitors = get_monitors()

    def get_screen_dimensions(self):
        """Gets the total screen dimensions across all monitors."""
        total_width = sum(monitor.width for monitor in self.monitors)
        max_height = max(monitor.height for monitor in self.monitors)
        return total_width, max_height

    def detect_active_monitor(self, x, y):
        """Detects which monitor the given coordinates fall into."""
        for monitor in self.monitors:
            if monitor.x <= x <= monitor.x + monitor.width and monitor.y <= y <= monitor.y + monitor.height:
                return monitor
        return None

    def adjust_for_active_monitor(self, x, y):
        """Adjusts coordinates for the active monitor."""
        monitor = self.detect_active_monitor(x, y)
        if monitor:
            adjusted_x = x - monitor.x
            adjusted_y = y - monitor.y
            return adjusted_x, adjusted_y
        return x, y  # Fallback if no active monitor is found
