# tests/test_pipeline.py
import io
import pytest
import torch
import librosa
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

MODEL_PATH = "backend/models/saved_model/ast_model.pt"

# --- Helper: create fake audio file ---
def fake_audio_file(sr=22050, duration=1.0):
    # Generate a sine wave for testing
    import numpy as np
    t = np.linspace(0, duration, int(sr*duration))
    y = 0.5 * np.sin(2 * np.pi * 440 * t)  # 440 Hz tone
    # Save to buffer as WAV
    import soundfile as sf
    buf = io.BytesIO()
    sf.write(buf, y, sr, format="WAV")
    buf.seek(0)
    return buf

# --- Test 1: Preprocessing Validation ---
def test_preprocessing_output_format():
    buf = fake_audio_file()
    y, sr = librosa.load(buf, sr=22050)
    assert isinstance(y, (list, tuple, torch.Tensor, np.ndarray))
    assert sr == 22050

# --- Test 2: Model Loading ---
def test_model_loading():
    try:
        model = torch.load(MODEL_PATH, map_location="cpu")
        assert model is not None
    except FileNotFoundError:
        pytest.skip("Model file not found, waiting for Member 1 to push ast_model.pt")

# --- Test 3: End-to-End /analyze ---
def test_analyze_endpoint():
    buf = fake_audio_file()
    file = {"file": ("test.wav", buf, "audio/wav")}
    response = client.post("/analyze", files=file)
    assert response.status_code == 200
    data = response.json()
    assert "deepfake_probability" in data
    assert isinstance(data["deepfake_probability"], float)
    assert 0.0 <= data["deepfake_probability"] <= 1.0
