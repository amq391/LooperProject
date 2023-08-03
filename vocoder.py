import librosa
import numpy as np
import pyaudio
import soundfile as sf

# Define the vocoder function
def vocoder(speech, modulator, window_size=1024, hop_length=512):
    # Ensure that the speech and modulator signals have the same length
    min_len = min(len(speech), len(modulator))
    speech = speech[:min_len]
    modulator = modulator[:min_len]

    # Compute the STFT (Short-Time Fourier Transform) of the modulator
    mod_stft = librosa.stft(modulator, n_fft=window_size, hop_length=hop_length)

    # Compute the magnitudes and phases of the speech signal
    speech_stft = librosa.stft(speech, n_fft=window_size, hop_length=hop_length)
    speech_mag, speech_phase = np.abs(speech_stft), np.angle(speech_stft)

    # Apply the modulator's magnitudes to the speech's phases
    vocoder_stft = speech_mag * np.exp(1j * ((np.angle(mod_stft))))

    # Inverse STFT to obtain the vocoded signal
    vocoded = librosa.istft(vocoder_stft, hop_length=hop_length)

    return vocoded

# Set up the audio stream for real-time processing
CHUNK_SIZE = 1024
SAMPLE_RATE = 44100

p = pyaudio.PyAudio()

def audio_callback(in_data, frame_count, time_info, status):
    # Convert the input data to numpy array
    speech = np.frombuffer(in_data, dtype=np.float32)

    # Process the speech using the modulator signal
    vocoded = vocoder(speech, modulator, window_size=1024, hop_length=512)


    # Convert the vocoded signal back to raw audio data
    output_data = vocoded.astype(np.float32).tobytes()

    return (output_data, pyaudio.paContinue)

# Load the modulator signal from file
modulator_file = 'saw.wav'
modulator, sr_modulator = librosa.load(modulator_file, sr=None)

# Load the modulator signal from librosa tone library
#tone = librosa.tone(100, sr=44100, length=4410)
#modulator = tone

# Load the modulator signal with a musical chord
#tone_a = librosa.tone(440, sr=44100, length=4410)
#tone_c_sharp = librosa.tone(554.37, sr=44100, length=4410)
#tone_e = librosa.tone(659.25, sr=44100, length=4410)

#tone_a_fft = librosa.stft(tone_a, n_fft=1024, hop_length=512)
#tone_c_sharp_fft = librosa.stft(tone_c_sharp, n_fft=1024, hop_length=512)
#tone_e_fft = librosa.stft(tone_e, n_fft=1024, hop_length=512)

#tone_fft = np.add(tone_a_fft, np.add(tone_c_sharp_fft, tone_e_fft))
#tone = librosa.istft(tone_fft, hop_length=512)

#modulator = tone

# Open the audio stream
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=SAMPLE_RATE,
                frames_per_buffer=CHUNK_SIZE,
                input=True,
                output=True,
                stream_callback=audio_callback)

# Start the audio stream
stream.start_stream()

# Keep the stream running for real-time processing
try:
    while stream.is_active():
        pass
except KeyboardInterrupt:
    # Stop the stream if interrupted by the user
    pass

# Stop and close the audio stream
stream.stop_stream()
stream.close()

p.terminate()