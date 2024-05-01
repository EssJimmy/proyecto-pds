import wave
import pyaudio
import sys
import sounddevice
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Sistema de reconocimiento de palabras")
        
        layout = QGridLayout(None)
        title = QLabel("Candado por voz")
        
        login = QPushButton("Acceder")
        login.clicked.connect(self.login_clicked)
        
        layout.addWidget(title, 0, 0, 1, 2)
        layout.addWidget(login, 1, 0)
        
        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)
        self.count = 1
        
        
    def login_clicked(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1 if sys.platform == 'darwin' else 2
        RATE = 44100
        RECORD_SECONDS = 5
        file_name = 'login_attempt' + self.count + '.wav'
        self.count += 1

        with wave.open(file_name, 'wb') as wf:
            p = pyaudio.PyAudio()
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            
            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

            print("Recording...")
            for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
                wf.writeframes(stream.read(CHUNK))

            print('Done')
            stream.close()
            p.terminate()

        self.show_message("Listo")

    def show_message(self, text: str):
        msg = QMessageBox()
        msg.setText(text)
        msg.exec()
        

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()