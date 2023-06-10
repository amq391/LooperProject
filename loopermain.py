from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

def start_recording_audio():
    print("Recording Audio...")

def stop_recording_audio():
    print("Recording Stopped!")

def main():
    app = QApplication([])
    window = QWidget()
    window.setGeometry(100, 100, 1000, 800)

    layout = QHBoxLayout()

    record_button = QPushButton("Record")
    record_button.clicked.connect(start_recording_audio)

    stop_recording_button = QPushButton("Stop")
    stop_recording_button.clicked.connect(stop_recording_audio)

    layout.addWidget(record_button)
    layout.addWidget(stop_recording_button)

    window.setLayout(layout)
    window.show()
    app.exec()

if __name__ == '__main__':
    main()