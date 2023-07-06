import pyaudio
import threading
from collections import deque
import numpy as np
from time import sleep
import librosa
import keyboard

class VoiceWarper:

    RATE = 38400
    CHUNK = int(RATE / 5)

    def __init__(self) -> None:
        self.chunks = 10
        self.instream = pyaudio.PyAudio().open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            )
        self.outstream = pyaudio.PyAudio().open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.RATE,
            output=True,
            )
        
    
        

    def _process_chunk(self):

        while True:


                
            raw_data = self.instream.read(self.CHUNK)
            

            decoded = np.frombuffer(raw_data, np.float32)
            m = np.fft.rfft(decoded)

            #new_m = np.roll(m,-100)
            #new_m[-100:] = 0
            new_s = np.roll(m,20)
            new_s[0:20] = 0

            #sum_arr = np.add(new_s, new_m)
            sum_n = np.fft.irfft(new_s)
            sum_n = sum_n.astype(np.float32)


            self.outstream.write(sum_n.tobytes())