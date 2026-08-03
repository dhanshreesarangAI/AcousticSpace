import librosa
import numpy as np
from audio_loader import load_audio

def detect_breathing(audio, sr):
    """
    Detects breathing patterns in audio signal
    """
    # Apply preemphasis filter to isolate breathing frequency range
    breathing_band = librosa.effects.preemphasis(audio)
    
    # Extract energy from audio signal
    energy = librosa.feature.rms(y=breathing_band)
    
    # Calculate average and standard deviation of energy
    avg_energy = np.mean(energy)
    std_energy = np.std(energy)
    
    return avg_energy, std_energy

def analyze_breathing_pattern(audio, sr):
    """
    Analyzes whether breathing pattern is natural or artificial
    """
    avg_energy, std_energy = detect_breathing(audio, sr)
    
    # Natural breathing has more energy variation than AI generated audio
    if std_energy > 0.02:
        pattern = "NATURAL"
    else:
        pattern = "UNNATURAL"
    
    result = {
        "breathing_pattern": pattern,
        "avg_energy": float(avg_energy),
        "std_energy": float(std_energy)
    }
    
    print(f"Breathing Pattern: {pattern}")
    print(f"Average Energy: {avg_energy:.4f}")
    print(f"Energy Variation: {std_energy:.4f}")
    
    return result