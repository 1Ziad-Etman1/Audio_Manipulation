import sounddevice as sd
from scipy.io.wavfile import write


fs = 44100  # Sample rate
seconds = 5  # Duration of recording

print("Recording...")
recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()
print("Recording complete.")

write("output.wav", fs, recording)