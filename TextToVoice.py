import io
import pygame
import time
from groq import Groq

class text_to_voice:
    def __init__(self):
        self.client = Groq(api_key="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")
        # Initialize pygame mixer
        pygame.mixer.init()

    def speak_text(self, text):
        model = "playai-tts"
        voice = "Fritz-PlayAI"
        response_format = "wav"

        # Get the response from Groq API
        response = self.client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
            response_format=response_format
        )
        
        # Create a temporary BytesIO object to hold the audio data
        audio_data = io.BytesIO()
        
        # Write the binary response data to our BytesIO object
        # BinaryAPIResponse can be read directly like a file
        audio_data.write(response.read())
        
        # Reset the position of the BytesIO object to the beginning
        audio_data.seek(0)
        
        # Load and play the audio directly from memory
        pygame.mixer.music.load(audio_data)
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)