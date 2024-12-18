import os
import subprocess


class TestRunner:
    """Handles dynamic discovery and execution of test files."""

    def __init__(self, test_dir="tests", output_widget=None):
        """
        Initialize the TestRunner.

        Args:
            test_dir (str): Directory containing test files.
            output_widget (tk.Text): Optional text widget for logging test output.
        """
        self.test_dir = test_dir
        self.output_widget = output_widget
        self.tests = self._discover_tests()

    def _discover_tests(self):
        """Scans the test directory for Python test files starting with 'test_'."""
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir, exist_ok=True)
            print(f"Created test directory: {self.test_dir}")
        return [f for f in os.listdir(self.test_dir) if f.startswith("test_") and f.endswith(".py")]

    def run_test(self, test_file):
        """Runs a single test file and logs its output."""
        test_path = os.path.join(self.test_dir, test_file)
        if not os.path.exists(test_path):
            self.log_output(f"Test file not found: {test_file}")
            return

        try:
            self.log_output(f"Running test: {test_file}")
            self.log_output("-" * 50)
            result = subprocess.run(["python", test_path], capture_output=True, text=True)
            self.log_output(result.stdout)
            if result.stderr:
                self.log_output(f"Errors:\n{result.stderr}")
            self.log_output(f"{'-' * 50}\nTest complete: {test_file}")
        except Exception as e:
            self.log_output(f"Error running test {test_file}: {e}")

    def log_output(self, message):
        """Logs output to the provided widget or prints it to the console."""
        if self.output_widget:
            self.output_widget.config(state="normal")
            self.output_widget.insert("end", message + "\n")
            self.output_widget.see("end")
            self.output_widget.config(state="disabled")
        else:
            print(message)
