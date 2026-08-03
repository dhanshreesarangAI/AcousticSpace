import librosa
import librosa.display
import matplotlib.pyplot as plt
audio_path = "../uploads/test.mp3"
audio,sample_rate = librosa.load(audio_path,sr=None)
mfcc = librosa.feature.mfcc(
    y=audio,
    sr=sample_rate,
    n_mfcc=13
)
print("MFCC shape :",mfcc.shape)
plt.figure(figsize=(12,5))
librosa.display.specshow(
    mfcc,
    x_axis="time",
    sr=sample_rate
)
plt.colorbar()
plt.title("MFCC Features")
plt.tight_layout()
plt.savefig("../uploads/mfcc.png")
plt.show()