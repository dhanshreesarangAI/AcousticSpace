import librosa
import numpy as np
from audio_loader import load_audio

def extract_mel_spectrogram(audio, sr):
    """
    Mel Spectrogram extract karta hai
    """
    mel_spec = librosa.feature.melspectrogram(
        y=audio, 
        sr=sr, 
        n_mels=128
    )
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    return mel_spec_db

def extract_rir_features(audio, sr):
    """
    Room Impulse Response features nikalta hai
    """
    spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)
    zero_crossing = librosa.feature.zero_crossing_rate(audio)
    
    rir_features = np.array([
        np.mean(spectral_centroid),
        np.mean(spectral_rolloff),
        np.mean(zero_crossing)
    ])
    return rir_features

def extract_all_features(file_path):
    """
    Sab features ek saath nikalta hai
    """
    audio, sr = load_audio(file_path)
    
    mel_spec = extract_mel_spectrogram(audio, sr)
    rir = extract_rir_features(audio, sr)
    
    print(f"Mel Spectrogram shape: {mel_spec.shape}")
    print(f"RIR Features: {rir}")
    
    return {
        "mel_spectrogram": mel_spec,
        "rir_features": rir
    }