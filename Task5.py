import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import get_window

def frame_signal(audio_path, frame_size_sec, overlap_sec, window_type='hamming'):
    # Step 1: Read the WAV file
    sample_rate, signal = wavfile.read(audio_path)
    signal = signal.astype(np.float32)

    # Convert stereo to mono if necessary
    if signal.ndim == 2:
        signal = signal.mean(axis=1)

    # Step 2: Convert durations to samples
    frame_length = int(frame_size_sec * sample_rate)
    overlap_length = int(overlap_sec * sample_rate)
    step = frame_length - overlap_length

    # Step 3: Calculate number of frames
    num_frames = 1 + int((len(signal) - frame_length) / step)

    # Step 4: Initialize frame matrix
    frames = np.zeros((num_frames, frame_length))

    # Step 5: Fill frames with overlapping segments and apply window
    window = get_window(window_type, frame_length, fftbins=False)

    for i in range(num_frames):
        start = i * step
        end = start + frame_length
        frames[i, :] = signal[start:end] * window

    # Step 6: Reconstruct framed signal
    reconstructed = np.zeros(step * (num_frames - 1) + frame_length)
    for i in range(num_frames):
        start = i * step
        reconstructed[start:start + frame_length] += frames[i]

    # Step 7: Plot original and framed signals
    time_original = np.linspace(0, len(signal) / sample_rate, num=len(signal))
    time_reconstructed = np.linspace(0, len(reconstructed) / sample_rate, num=len(reconstructed))

    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(time_original, signal, label='Original Signal')
    plt.title('Original Signal')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')

    plt.subplot(2, 1, 2)
    plt.plot(time_reconstructed, reconstructed, label='Framed Signal', color='orange')
    plt.title('Framed Signal (Reconstructed)')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')

    plt.tight_layout()
    # plt.show()
    plt.savefig("framed_vs_original.png")

    return frames

# Example usage
frames = frame_signal(
    audio_path='output.wav',
    frame_size_sec=0.025,   # 25 ms
    overlap_sec=0.0125,     # 50% overlap
    window_type='hann'
)

print(f"Number of frames: {frames.shape[0]}")
print(f"Frame size (samples): {frames.shape[1]}")
print("First frame:\n", frames[0:5])
