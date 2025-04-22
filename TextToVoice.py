import pygame
from groq import Groq
import time as time
import os 
os.makedirs("speeches", exist_ok=True)
class text_to_voice:
    def __init__(self):
        self.client = Groq(api_key="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")

    def speak_text(self,text):
        speech_file_path = f"speeches/speech{time.time()}.wav"
        model = "playai-tts"
        voice = "Fritz-PlayAI"
        response_format = "wav"

        response = self.client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
            response_format=response_format
        )

        response.write_to_file(speech_file_path)

        pygame.mixer.init()
        pygame.mixer.music.load(speech_file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        # if os.path.exists(speech_file_path):
        #     os.remove(speech_file_path)
