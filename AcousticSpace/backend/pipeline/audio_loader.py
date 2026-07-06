import librosa
import numpy as np

def load_audio(file_path, sample_rate=22050):
    """
    Audio file load karta hai
    Returns: audio signal aur sample rate
    """
    audio, sr = librosa.load(file_path, sr=sample_rate)
    print(f"Audio loaded: {file_path}")
    print(f"Sample rate: {sr}")
    print(f"Duration: {len(audio)/sr:.2f} seconds")
    return audio, sr

def get_audio_info(file_path):
    """
    Audio file ki basic info return karta hai
    """
    audio, sr = load_audio(file_path)
    info = {
        "sample_rate": sr,
        "duration": len(audio)/sr,
        "samples": len(audio)
    }
    return info