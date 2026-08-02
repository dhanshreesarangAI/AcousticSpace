import librosa
import numpy as np
from audio_loader import load_audio

def detect_syllables(audio, sr):
    """
    Detect syllable boundaries in audio
    """
    # Extract onset strength
    onset_env = librosa.onset.onset_strength(y=audio, sr=sr)
    
    # Detect onset frames
    onsets = librosa.onset.onset_detect(
        onset_envelope=onset_env,
        sr=sr,
        units='time'
    )
    
    return onsets

def detect_breath_points(audio, sr):
    """
    Detect breathing points in audio
    """
    # Extract RMS energy
    rms = librosa.feature.rms(y=audio)[0]
    
    # Find low energy points — these are breathing points
    threshold = np.mean(rms) * 0.3
    breath_frames = np.where(rms < threshold)[0]
    
    # Convert frames to time
    breath_times = librosa.frames_to_time(breath_frames, sr=sr)
    
    return breath_times

def check_cadence_alignment(audio, sr):
    """
    Check if breathing aligns with syllable patterns
    """
    syllables = detect_syllables(audio, sr)
    breath_points = detect_breath_points(audio, sr)
    
    if len(syllables) == 0 or len(breath_points) == 0:
        return {
            "alignment": "UNKNOWN",
            "syllable_count": 0,
            "breath_count": 0,
            "cadence_score": 0.0
        }
    
    # Calculate alignment score
    aligned_count = 0
    for breath in breath_points:
        # Check if breath point is near any syllable boundary
        distances = np.abs(syllables - breath)
        min_distance = np.min(distances)
        
        # Natural breathing happens between syllables
        if min_distance < 0.1:
            aligned_count += 1
    
    # Calculate cadence score
    cadence_score = aligned_count / len(breath_points)
    
    # Determine if alignment is natural or artificial
    if cadence_score > 0.5:
        alignment = "NATURAL"
    else:
        alignment = "ARTIFICIAL"
    
    result = {
        "alignment": alignment,
        "syllable_count": len(syllables),
        "breath_count": len(breath_points),
        "cadence_score": round(cadence_score, 4)
    }
    
    print(f"Syllables detected: {len(syllables)}")
    print(f"Breath points detected: {len(breath_points)}")
    print(f"Cadence alignment: {alignment}")
    print(f"Cadence score: {cadence_score:.4f}")
    
    return result