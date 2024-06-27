import sys
import math
import pygame
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QSlider
from PyQt5.QtCore import Qt, QTimer
pygame.mixer.init()
def generate_sine_wave(volume):
    sample_rate = 44100 
    duration = 1.0  
    frequency = 1 
    num_samples = int(sample_rate * duration)
    max_amplitude = 2 ** 15 - 1
    samples = []
    for i in range(num_samples):
        sample = math.sin(2 * math.pi * frequency * i / sample_rate)
        samples.append(int(sample * volume * max_amplitude))
    samples_bytes = bytearray()
    for sample in samples:
        samples_bytes.extend(sample.to_bytes(2, byteorder='little', signed=True))
    sound = pygame.mixer.Sound(buffer=samples_bytes)
    return sound
sine_wave = generate_sine_wave(0.01)
def play_sine_wave():
    pygame.mixer.Channel(0).play(sine_wave, loops=-1)
def stop_sine_wave():
    pygame.mixer.Channel(0).stop()
def quit_application():
    pygame.mixer.quit()
    app.quit()  
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sine Wave Player")
        self.setGeometry(100, 100, 400, 50) 
        layout = QVBoxLayout()
        self.play_button = QPushButton('Start/Stop', self)
        self.play_button.clicked.connect(self.start_or_stop)
        layout.addWidget(self.play_button)
        self.status_label = QLabel('Stopped')
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        self.setLayout(layout)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status_label)
        self.timer.start(500)
        self.update_status_label()
    def update_volume(self, value):
        volume = float(value) / 100.0 * 0.01 
        sine_wave.set_volume(volume)
        self.volume_value_label.setText(f'Volume: {volume:.2f}')
    def start_or_stop(self):
        if pygame.mixer.Channel(0).get_busy():
            stop_sine_wave()
        else:
            play_sine_wave()
        self.update_status_label()
    def update_status_label(self):
        if pygame.mixer.Channel(0).get_busy():
            self.status_label.setText('Running')
            self.status_label.setStyleSheet('color: green; font-weight: bold;')
        else:
            self.status_label.setText('Stopped')
            self.status_label.setStyleSheet('color: red; font-weight: bold;')
    def closeEvent(self, event):
        stop_sine_wave() 
        quit_application() 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
pygame.mixer.quit()
