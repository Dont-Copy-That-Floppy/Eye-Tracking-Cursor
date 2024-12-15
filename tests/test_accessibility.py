# test_accessibility.py
import unittest
from accessibility import Accessibility


class TestAccessibility(unittest.TestCase):
    """Unit tests for the Accessibility module."""

    def setUp(self):
        """Set up test instance."""
        self.accessibility = Accessibility()

    def test_speak(self):
        """Test that speak does not raise exceptions."""
        try:
            self.accessibility.speak("Test message.")
        except Exception as e:
            self.fail(f"speak() raised an exception: {e}")

    def test_list_voices(self):
        """Test listing available voices."""
        voices = self.accessibility.list_voices()
        self.assertIsInstance(voices, list)
        self.assertGreater(len(voices), 0)


if __name__ == "__main__":
    unittest.main()
