import React, { useState } from "react";

function AudioAnalyzer() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!file) {
      alert("Please select a WAV file first.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to analyze audio");
      }

      const data = await response.json();
      setResult(data.deepfake_probability);
    } catch (error) {
      console.error(error);
      alert("Error analyzing audio");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Deepfake Audio Analyzer</h2>
      <input type="file" accept=".wav" onChange={handleFileChange} />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Analyzing..." : "Upload & Analyze"}
      </button>
      {result !== null && (
        <p>
          Deepfake Probability: <strong>{result.toFixed(3)}</strong>
        </p>
      )}
    </div>
  );
}

export default AudioAnalyzer;
import React from "react";
import AudioAnalyzer from "./components/AudioAnalyzer";

function App() {
  return (
    <div>
      <h1>AcousticSpace Frontend</h1>
      <AudioAnalyzer />
    </div>
  );
}

export default App;
