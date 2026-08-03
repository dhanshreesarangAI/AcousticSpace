import librosa

audio_path = "../uploads/test.mp3"

audio,sample_rate = librosa.load(audio_path,sr=None)

print("Sample rate :",sample_rate)
print("Total samples :",len(audio))
print("First 10 samples :")
print(audio[:10])