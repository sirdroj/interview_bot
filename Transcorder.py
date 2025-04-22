import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import threading
import queue
import tempfile
import os
from groq import Groq

class Transcorder:
    def __init__(self, api_key, sample_rate=44100, channels=1):
        self.api_key = api_key
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.q = queue.Queue()
        self.thread = None
        self.temp_wav = None
        self.client = Groq(api_key=self.api_key)
        self.transcript = ""

    def _callback(self, indata, frames, time, status):
        if self.recording:
            self.q.put(indata.copy())

    def _record_audio(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            self.temp_wav = f.name
        with sd.InputStream(samplerate=self.sample_rate, channels=self.channels, callback=self._callback):
            frames = []
            while self.recording:
                try:
                    frames.append(self.q.get(timeout=1))
                except queue.Empty:
                    pass
            if frames:
                audio_np = np.concatenate(frames, axis=0)
                write(self.temp_wav, self.sample_rate, audio_np)

    def start_recording(self):
        self.recording = True
        self.thread = threading.Thread(target=self._record_audio)
        self.thread.start()
        print("Recording started...")

    def stop_recording(self):
        self.recording = False
        self.thread.join()
        print("Recording stopped.")

        if not self.temp_wav or not os.path.exists(self.temp_wav):
            raise RuntimeError("No audio file recorded.")

        with open(self.temp_wav, "rb") as f:
            response = self.client.audio.transcriptions.create(
                file=(self.temp_wav, f.read()),
                model="whisper-large-v3",
                response_format="verbose_json"
            )
            self.transcript = response.text

        os.remove(self.temp_wav)  # Clean up
        return self.transcript
