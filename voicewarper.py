import pyaudio
import threading
from collections import deque
import numpy as np
from time import sleep
import librosa
import keyboard

class VoiceWarper:

    RATE = 44100
    CHUNK = int(RATE / 10)

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
        tone = librosa.tone(440,sr=44100,length=4410)
        tone_fft = np.fft.rfft(tone)

        while True:


                
            raw_data = self.instream.read(self.CHUNK)
            

            mod_sig = np.frombuffer(raw_data, np.float32)
            mod_sig_fft = np.fft.rfft(mod_sig)

            tone_fft_copy = np.copy(tone_fft)

            bp_one = mod_sig_fft[0:147]
            bp_two = mod_sig_fft[147:294]
            bp_three = mod_sig_fft[294:441]
            bp_four = mod_sig_fft[441:588]
            bp_five = mod_sig_fft[588:735]
            bp_six = mod_sig_fft[735:882]
            bp_seven = mod_sig_fft[882:1029]
            bp_eight = mod_sig_fft[1029:1176]
            bp_nine = mod_sig_fft[1176:1323]
            bp_ten = mod_sig_fft[1323:1470]
            bp_eleven = mod_sig_fft[1470:1617]
            bp_twelve = mod_sig_fft[1617:1764]
            bp_thirteen = mod_sig_fft[1764:1911]
            bp_fourteen = mod_sig_fft[1911:2058]
            bp_fifteen = mod_sig_fft[2058:2205]

            bp_one = np.amax(bp_one)
            bp_two = np.amax(bp_two)
            bp_three = np.amax(bp_three)
            bp_four = np.amax(bp_four)
            bp_five = np.amax(bp_five)
            bp_six = np.amax(bp_six)
            bp_seven = np.amax(bp_seven)
            bp_eight = np.amax(bp_eight)
            bp_nine = np.amax(bp_nine)
            bp_ten = np.amax(bp_ten)
            bp_eleven = np.mean(bp_eleven)
            bp_twelve = np.amax(bp_twelve)
            bp_thirteen = np.amax(bp_thirteen)
            bp_fourteen = np.amax(bp_fourteen)
            bp_fifteen = np.amax(bp_fifteen)
                
            tone_fft_copy[0:147] = bp_one
            tone_fft_copy[147:294] = bp_two
            tone_fft_copy[294:441] = bp_three
            tone_fft_copy[441:588] = bp_four
            tone_fft_copy[588:735] = bp_five
            tone_fft_copy[735:882] = bp_six
            tone_fft_copy[882:1029] = bp_seven
            tone_fft_copy[1029:1176] = bp_eight
            tone_fft_copy[1176:1323] = bp_nine
            tone_fft_copy[1323:1470] = bp_ten
            tone_fft_copy[1470:1617] = bp_eleven
            tone_fft_copy[1617:1764] = bp_twelve
            tone_fft_copy[1764:1911] = bp_thirteen
            tone_fft_copy[1911:2058] = bp_fourteen
            tone_fft_copy[2058:2205] = bp_fifteen
            

            #new_m = np.roll(m,-100)
            #new_m[-100:] = 0
            #new_s = np.roll(m,20)
            #new_s[0:20] = 0

            #sum_arr = np.add(new_s, new_m)
            sum_n = np.fft.irfft(tone_fft_copy)
            sum_n = sum_n.astype(np.float32)


            self.outstream.write(sum_n.tobytes())