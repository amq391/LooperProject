import pyaudio
import numpy as np
import keyboard

class VoiceWarper:

    RATE = 44100
    CHUNK = int(RATE / 10)

    def __init__(self) -> None:
        self.chunks = 10
        self.stream = pyaudio.PyAudio().open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
            )
        
    
    def _process_chunk(self):
        while True:
            raw_data = self.stream.read(self.CHUNK)
            mod_sig = np.frombuffer(raw_data, np.float32)
            mod_sig_fft = np.fft.rfft(mod_sig)
            lower_mod_sig_fft = np.roll(mod_sig_fft,-40)
            lower_mod_sig_fft[-40:] = 0
            higher_mod_sig_fft = np.roll(mod_sig_fft,40)
            higher_mod_sig_fft[0:40] = 0
            warped_vocal_fft = np.add(higher_mod_sig_fft, lower_mod_sig_fft)
            warped_vocal = np.fft.irfft(warped_vocal_fft)
            warped_vocal = warped_vocal.astype(np.float32)
            self.stream.write(warped_vocal.tobytes())