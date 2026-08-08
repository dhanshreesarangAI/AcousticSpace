import sys
sys.path.append('../models')
from audio_loader import load_audio
from feature_extractor import extract_all_features
from breathing_detector import analyze_breathing_pattern
from breathing_cadence import analyze_cadence_alignment
from model import AcousticSpaceModel

def predict_audio(file_path):
    """
    Complete prediction pipeline for audio file
    """
    print(f"Analyzing: {file_path}")
    print("---")

    # Step 1 — Load audio
    audio, sr = load_audio(file_path)

    # Step 2 — Extract features
    features = extract_all_features(file_path)

    # Step 3 — Analyze breathing pattern
    breathing = analyze_breathing_pattern(audio, sr)

    # Step 4 — Analyze cadence alignment
    cadence = analyze_cadence_alignment(file_path)

    # Step 5 — Get model prediction
    model = AcousticSpaceModel()
    prediction = model.predict(audio, sr)

    # Step 6 — Combine all results
    final_result = {
        "prediction": prediction["prediction"],
        "confidence_score": prediction["confidence_score"],
        "real_probability": prediction["real_probability"],
        "fake_probability": prediction["fake_probability"],
        "rir_mismatch": "HIGH" if prediction["fake_probability"] > 50 else "LOW",
        "breathing": breathing["breathing_pattern"],
        "cadence_alignment": cadence["cadence_alignment"],
        "syllable_count": cadence["syllable_count"]
    }

    print("---")
    print(f"FINAL RESULT: {final_result['prediction']}")
    print(f"Confidence Score: {final_result['confidence_score']}%")
    print(f"Breathing: {final_result['breathing']}")
    print(f"Cadence: {final_result['cadence_alignment']}")
    print(f"RIR Mismatch: {final_result['rir_mismatch']}")

    return final_result

if __name__ == "__main__":
    result = predict_audio("test_audio.wav")
