from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from pvrecorder import PvRecorder
import wave, struct
from playsound import playsound




def start_recording_audio():
    print("Recording Audio...")
    recorder = PvRecorder(device_index=0, frame_length=512)
    audio = []

    try:
        recorder.start()
        while True:
            frame = recorder.read()
            audio.extend(frame)
    except KeyboardInterrupt:
        recorder.stop()
        with wave.open('sample.wav', 'w') as f:
            f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(audio), *audio))
            
    finally:
        recorder.delete()
        print("sample recorded and saved")


def stop_recording_audio():
    print("Recording Stopped!")

def playback_audio():
    print("Playing recorded audio...")
    #with wave.open('sample.wav', 'r') as f:
    playsound('sample.wav')

def main():
    app = QApplication([])
    window = QWidget()
    window.setGeometry(100, 100, 1000, 800)

    layout = QHBoxLayout()

    record_button = QPushButton("Record")
    record_button.clicked.connect(start_recording_audio)

    stop_recording_button = QPushButton("Stop")
    stop_recording_button.clicked.connect(stop_recording_audio)

    playback_button = QPushButton("Play")
    playback_button.clicked.connect(playback_audio)

    layout.addWidget(record_button)
    layout.addWidget(stop_recording_button)
    layout.addWidget(playback_button)

    window.setLayout(layout)
    window.show()
    app.exec()

if __name__ == '__main__':
    main()