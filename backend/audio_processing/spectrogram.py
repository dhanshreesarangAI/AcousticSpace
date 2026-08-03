import librosa
import librosa.display
import matplotlib.pyplot as plt 
import numpy as np 
audio_path = "../uploads/test.mp3"
audio,sample_rate = librosa.load(audio_path,sr=None)
spectrogram = librosa.feature.melspectrogram(
    y = audio,
    sr = sample_rate
)
spectrogram_db = librosa.power_to_db(
    spectrogram,
    ref=np.max
)
plt.figure(figsize=(12,4))
librosa.display.specshow(
    spectrogram_db,
    sr= sample_rate,
    x_axis="time",
    y_axis="mel"
)
plt.colorbar(format= "%+2.0f dB")
plt.title("Mel spectrogram")
plt.tight_layout()
plt.show()

