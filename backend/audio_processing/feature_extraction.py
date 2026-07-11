import librosa
import numpy as np
audio_path = "../uploads/test.mp3"
audio,sample_rate = librosa.load(audio_path,sr=None)
mfcc = librosa.feature.mfcc(
    y=audio,
    sr=sample_rate,
    n_mfcc=13
)
zcr=librosa.feature.zero_crossing_rate(audio)
rms=librosa.feature.rms(y=audio)
spectral_centroid = librosa.feature.spectral_centroid(
    y=audio,
    sr=sample_rate
)

print("MFCC shape : ",mfcc.shape)
print("ZCR shape : ",zcr.shape)
print("RMS shape : ",rms.shape)
print("Spectral Centroid Shape : ",spectral_centroid.shape)

print("\nAverage Values \n")

print("MFCC shape : ",np.mean(mfcc))
print("ZCR shape : ",np.mean(zcr))
print("RMS shape : ",np.mean(rms))
print("Spectral Centroid Shape : ",np.mean(spectral_centroid))

