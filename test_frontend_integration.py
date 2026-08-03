import io
import pytest
import requests
import numpy as np
import soundfile as sf

API_URL = "http://127.0.0.1:8000/analyze"

def fake_audio_file(sr=22050, duration=1.0):
    """Generate a simple sine wave audio buffer for testing."""
    t = np.linspace(0, duration, int(sr*duration))
    y = 0.5 * np.sin(2 * np.pi * 440 * t)
    buf = io.BytesIO()
    sf.write(buf, y, sr, format="WAV")
    buf.seek(0)
    return buf

def test_frontend_like_call():
    """Simulate frontend sending audio to backend via HTTP POST."""
    buf = fake_audio_file()
    files = {"file": ("test.wav", buf, "audio/wav")}
    response = requests.post(API_URL, files=files)

    assert response.status_code == 200
    data = response.json()
    assert "deepfake_probability" in data
    assert isinstance(data["deepfake_probability"], float)
    assert 0.0 <= data["deepfake_probability"] <= 1.0
import pytest
import sys

def main():
    
    print(" Running pipeline tests...")
    result_pipeline = pytest.main(["tests/test_pipeline.py", "-v"])
    if result_pipeline != 0:
        print("❌ Pipeline tests failed")
        sys.exit(result_pipeline)

    
    print("\n Running frontend integration tests...")
    result_frontend = pytest.main(["tests/test_frontend_integration.py", "-v"])
    if result_frontend != 0:
        print("❌ Frontend integration tests failed")
        sys.exit(result_frontend)

    print("\n✅ All tests passed successfully!")

if __name__ == "__main__":
    main()
python run_all_tests.py

