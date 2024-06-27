import sys
import math
import pygame
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QSlider
from PyQt5.QtCore import Qt, QTimer

# Initialize pygame audio
pygame.mixer.init()

# Function to generate a near-silent sine wave
def generate_sine_wave(volume):
    sample_rate = 44100  # Standard audio sample rate
    duration = 1.0  # Duration in seconds
    frequency = 1  # Frequency of the sine wave (440 Hz)
    
    num_samples = int(sample_rate * duration)
    max_amplitude = 2 ** 15 - 1  # Maximum amplitude for 16-bit audio

    # Generate sine wave samples
    samples = []
    for i in range(num_samples):
        sample = math.sin(2 * math.pi * frequency * i / sample_rate)
        samples.append(int(sample * volume * max_amplitude))

    # Convert samples to 16-bit format (bytes)
    samples_bytes = bytearray()
    for sample in samples:
        samples_bytes.extend(sample.to_bytes(2, byteorder='little', signed=True))

    # Create pygame sound object
    sound = pygame.mixer.Sound(buffer=samples_bytes)
    return sound

# Initialize the sine wave sound
sine_wave = generate_sine_wave(0.01)  # Start with a very low volume

# Function to play the sine wave on loop
def play_sine_wave():
    pygame.mixer.Channel(0).play(sine_wave, loops=-1)

# Function to stop the sine wave playback
def stop_sine_wave():
    pygame.mixer.Channel(0).stop()

# Function to properly quit pygame and PyQt5 application
def quit_application():
    pygame.mixer.quit()  # Quit pygame mixer
    app.quit()  # Quit PyQt5 application

# PyQt5 Application
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sine Wave Player")
        self.setGeometry(100, 100, 400, 50)  # Set window position and size
        
        layout = QVBoxLayout()

        # Play button
        self.play_button = QPushButton('Start/Stop', self)
        self.play_button.clicked.connect(self.start_or_stop)
        layout.addWidget(self.play_button)







        # Status label (running/stopped)
        self.status_label = QLabel('Stopped')
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        # Timer to update status label
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status_label)
        self.timer.start(500)  # Update every 500 milliseconds

        # Initial status
        self.update_status_label()

    # Function to update volume based on slider value
    def update_volume(self, value):
        volume = float(value) / 100.0 * 0.01  # Adjust volume calculation
        sine_wave.set_volume(volume)
        self.volume_value_label.setText(f'Volume: {volume:.2f}')

    # Function to start or stop sine wave playback
    def start_or_stop(self):
        if pygame.mixer.Channel(0).get_busy():
            stop_sine_wave()
        else:
            play_sine_wave()

        self.update_status_label()

    # Function to update the status label based on sine wave playback state
    def update_status_label(self):
        if pygame.mixer.Channel(0).get_busy():
            self.status_label.setText('Running')
            self.status_label.setStyleSheet('color: green; font-weight: bold;')
        else:
            self.status_label.setText('Stopped')
            self.status_label.setStyleSheet('color: red; font-weight: bold;')

    # Override closeEvent to properly quit pygame and application
    def closeEvent(self, event):
        stop_sine_wave()  # Stop sine wave playback
        quit_application()  # Quit application

# Main function to run PyQt5 application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# Clean up pygame resources (normally not reached due to sys.exit())
pygame.mixer.quit()
