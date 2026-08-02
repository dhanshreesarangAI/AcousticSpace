import { useState } from "react";
import "./UploadCard.css";
import Waveform from "../Waveform/Waveform";
import { analyzeAudio } from "../../services/api";
import ResultCard from "../ResultCard/ResultCard";

function UploadCard({ onAnalysisComplete }) {

    const [selectedFile, setSelectedFile] = useState(null);
    const [audioURL, setAudioURL] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleFileChange = (event) => {

        const file = event.target.files[0];

        if (file) {
            setSelectedFile(file);
            setAudioURL(URL.createObjectURL(file));

            // Clear previous result/error
            setResult(null);
            setError("");
        }
    };

    const handleAnalyze = async () => {

        if (!selectedFile) {
            setError("Please select an audio file.");
            return;
        }

        try {

            setLoading(true);
            setError("");

            const response = await analyzeAudio(selectedFile);

            // Show result
            setResult(response);

            // Save result to History
            if (onAnalysisComplete) {
                onAnalysisComplete(
                    response,
                    selectedFile.name
                );
            }

        } catch (error) {

            console.log(error);

            setError(
                error.message || "Audio analysis failed. Please try again."
            );

        } finally {

            setLoading(false);

        }
    };

    const resetAll = () => {

        setSelectedFile(null);
        setAudioURL(null);
        setResult(null);
        setError("");

        // Reset file input
        const input = document.getElementById("audioInput");

        if (input) {
            input.value = "";
        }
    };

    return (

        <div className="card">

            <h2>Upload Audio</h2>

            <p>
                Upload an audio file to detect whether it is
                <strong> Real </strong>
                or
                <strong> AI Generated</strong>.
            </p>

            {/* File Upload */}

            <input
                id="audioInput"
                type="file"
                accept=".mp3,.wav,.m4a"
                onChange={handleFileChange}
            />

            {/* Selected File */}

            {selectedFile && (

                <div className="file-info">

                    <p>
                        <strong>Selected File:</strong>
                    </p>

                    <p>
                        {selectedFile.name}
                    </p>

                    {/* Audio Preview */}

                    <audio
    id="audio-player"
    controls
    src={audioURL}
>
    Your browser does not support the audio element.
</audio>

<Waveform audioURL={audioURL} />

                </div>
            )}

            {/* Error Message */}

            {error && (

                <p className="error-message">
                    ❌ {error}
                </p>

            )}

            {/* Analyze Button */}

            <button
                onClick={handleAnalyze}
                disabled={loading}
            >
                {loading
                    ? "Analyzing..."
                    : "Analyze Audio"
                }
            </button>

            {/* Loading */}

            {loading && (

                <p className="loading-message">
                    ⏳ Analyzing...
                </p>

            )}

            {/* Result */}

            {result && (

                <>

                    <ResultCard
                        result={result}
                    />

                    {/* Reset Button */}

                    <button
                        onClick={resetAll}
                    >
                        Choose Another File
                    </button>

                </>

            )}

        </div>

    );
}

export default UploadCard;