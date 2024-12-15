import pyttsx3


class Accessibility:
    """Handles accessibility features like voice feedback."""

    def __init__(self):
        self.engine = pyttsx3.init()

        # Default voice settings
        self.rate = 150  # Words per minute
        self.volume = 1.0  # Maximum volume
        self.voice_id = None  # Defaults to the system's default voice

        # Apply default settings
        self.configure_voice()

    def configure_voice(self, rate=None, volume=None, voice_id=None):
        """Configures the text-to-speech engine."""
        if rate is not None:
            self.rate = rate
            self.engine.setProperty("rate", self.rate)

        if volume is not None:
            self.volume = volume
            self.engine.setProperty("volume", self.volume)

        if voice_id is not None:
            self.voice_id = voice_id
            self.engine.setProperty("voice", self.voice_id)
        else:
            # If no specific voice is set, use the first available voice
            voices = self.engine.getProperty("voices")
            if voices:
                self.voice_id = voices[0].id
                self.engine.setProperty("voice", self.voice_id)

    def list_voices(self):
        """Lists all available voices."""
        voices = self.engine.getProperty("voices")
        return [(voice.id, voice.name) for voice in voices]

    def speak(self, message):
        """Speak a message using text-to-speech."""
        try:
            self.engine.say(message)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech: {e}")

    def stop(self):
        """Stops any ongoing speech."""
        self.engine.stop()
