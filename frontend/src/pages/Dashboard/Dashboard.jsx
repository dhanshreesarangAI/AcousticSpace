import "./Dashboard.css";
import { useState } from "react";

function Dashboard() {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (file) {
      setSelectedFile(file);
    }
  };

  return (
    <div className="dashboard">

      <header className="header">
        <h1>🎙️ AcousticSpace</h1>
        <p>AI Powered Deepfake Audio Detection</p>
      </header>

      <div className="card">

        <h2>Upload Audio</h2>

        <p>
          Upload an audio file to detect whether it is
          <strong> Real </strong>
          or
          <strong> AI Generated</strong>.
        </p>

        <input
          type="file"
          accept=".mp3,.wav,.m4a"
          onChange={handleFileChange}
        />

        {selectedFile && (
          <div className="file-info">
            <p><strong>Selected File:</strong></p>
            <p>{selectedFile.name}</p>
          </div>
        )}

      </div>

    </div>
  );
}

export default Dashboard;