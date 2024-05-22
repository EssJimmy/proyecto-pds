import wave
import pyaudio
import sys
import sounddevice
from recognition import recognition
from os import path
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Sistema de reconocimiento de palabras")
        
        layout = QGridLayout(None)
        title = QLabel("Candado por voz")
        
        self.login = QPushButton("Acceder")
        self.login.clicked.connect(self.login_clicked)
        self.set_key = QPushButton("Definir contraseña")
        self.set_key.clicked.connect(self.key_clicked)

        layout.addWidget(title, 0, 0, 1, 2)
        layout.addWidget(self.login, 1, 0)
        layout.addWidget(self.set_key, 1, 1)
        
        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)
        self.count = 1
        
        
    def login_clicked(self) -> None:
        self.show_message("Al presionar OK empezará la grabación")
        file_name = self.record()
        self.count += 1 
        self.show_message("Listo")
        
        if path.isfile('./key.wav'):
            if recognition(file_name, 'key.wav'):
                self.show_message("Contraseña correcta")
            else:
                self.show_message(f"Contraseña incorrecta, te quedan {5 - self.count} intentos")
                if (5 - self.count) == 0:
                    self.show_message("Deberas esperar treinta segundos despues de presionar Ok para volver a intentarlo")
                    self.login.setEnabled(False)
                    QTimer.singleShot(30000, lambda: self.login.setDisabled(False))
                    self.count = 0
        else:
            self.show_message("Por favor establece la contraseña primero")
    

    def key_clicked(self) -> None:
        self.show_message("Al presionar OK empezará la grabación")
        self.record('key')
        self.show_message("Listo")
    

    def record(self, name='login_attempt') -> str:
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1 if sys.platform == 'darwin' else 2
        RATE = 44100
        RECORD_SECONDS = 5
        file_name = name + str(self.count) + '.wav' if name == 'login_attempt' else name + '.wav'

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
        
        return file_name


    def show_message(self, text: str) -> None:
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

