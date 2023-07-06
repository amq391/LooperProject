import pyaudio
import numpy as np
from collections import deque
import threading
from time import sleep



class AudioBuffer:

    RATE = 44100
    CHUNK = int(RATE / 10)
    
    def __init__(self, chunks: int = 5) -> None:
        self.chunks = chunks
        self.stream = pyaudio.PyAudio().open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            )
        self.outstream = pyaudio.PyAudio().open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.RATE,
            output=True,
            )
        self.thread = threading.Thread(target=self._collect_data, daemon=True)
        self.frames = deque(maxlen=self.chunks)

    def __call__(self):
        return np.concatenate(self.frames)
    
    def __len__(self):
        return self.CHUNK * self.chunks
    
    def is_full(self):
        return len(self.frames) == self.chunks
    
    def start(self):
        self.thread.start()
        while not self.is_full(): # wait until the buffer is filled
            sleep(0.1)

    
    def _collect_data(self):
        while True:
            raw_data = self.stream.read(self.CHUNK)
            

            decoded = np.frombuffer(raw_data, np.int16)
            m = np.fft.rfft(decoded)
            new_m = np.roll(m,-40)
            new_m[-40:] = 0
            new_s = np.roll(m,40)
            new_s[0:40] = 0
            sum_arr = np.add(new_s, new_m)
            sum_n = np.fft.irfft(sum_arr)
            sum_n = sum_n.astype(np.int16)


            self.outstream.write(sum_n.tobytes())

            
            self.frames.append(decoded)

        


if __name__ == "__main__":
    audio_buffer = AudioBuffer()
    audio_buffer.start()
    print(audio_buffer().shape)