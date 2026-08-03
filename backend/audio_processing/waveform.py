import librosa
import librosa.display
import matplotlib.pyplot as plt

audio_path = "../uploads/test.mp3"

audio,sample_rate = librosa.load(audio_path,sr=None)

plt.figure(figsize=(12,4))

librosa.display.waveshow(audio,sr=sample_rate)
plt.title("Audio Wave")
plt.xlabel("Seconds")
plt.ylabel("Amplitude")

plt.show()
