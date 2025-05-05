import numpy as np
from scipy.io import wavfile
import sounddevice as sd
import os

# Load WAV file
file_path = 'output.wav'  # Update path if needed
samplerate, data = wavfile.read(file_path)

# Get number of samples
num_samples = data.shape[0]

# Check number of channels (mono or stereo)
num_channels = 1 if data.ndim == 1 else data.shape[1]

# Get bits per sample from dtype
bits_per_sample = data.dtype.itemsize * 8

# Total data size in bits
total_data_bits = num_samples * num_channels * bits_per_sample

# Bit rate = sample rate * bits per sample * number of channels
bit_rate = samplerate * bits_per_sample * num_channels

# Type of recording
recording_type = 'Mono' if num_channels == 1 else 'Stereo'

# Print all results
print(f"Number of samples: {num_samples}")
print(f"Data size in bits: {total_data_bits} bits")
print(f"Bits per sample: {bits_per_sample}")
print(f"Bit rate: {bit_rate} bps")
print(f"Type of recording: {recording_type}")
print(f"Sampling rate: {samplerate} Hz")

# Reverse the audio
reversed_data = data[::-1]

# Play the audio
print("Playing audio...")
sd.play(data, samplerate)
sd.wait()
# Play the reversed audio
print("Playing reversed audio...")
sd.play(reversed_data, samplerate)
sd.wait()
