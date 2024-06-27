import sys
import math
import pygame
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QSlider
from PyQt5.QtCore import Qt

# Initialize pygame audio
pygame.mixer.init()

# Function to generate a near-silent sine wave
def generate_sine_wave(volume):
    sample_rate = 44100  # Standard audio sample rate
    duration = 1.0  # Duration in seconds
    frequency = 440  # Frequency of the sine wave (440 Hz)
    
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
        self.setGeometry(100, 100, 300, 200)  # Set window position and size
        
        layout = QVBoxLayout()

        # Play button
        self.play_button = QPushButton('Play', self)
        self.play_button.clicked.connect(play_sine_wave)
        layout.addWidget(self.play_button)

        # Stop button
        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(stop_sine_wave)
        layout.addWidget(self.stop_button)

        # Volume slider
        self.volume_label = QLabel('Volume')
        layout.addWidget(self.volume_label)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(1)
        self.volume_slider.valueChanged.connect(self.update_volume)
        layout.addWidget(self.volume_slider)

        self.setLayout(layout)

    # Function to update volume based on slider value
    def update_volume(self, value):
        volume = float(value) / 100.0
        sine_wave.set_volume(volume)

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
