import "./Dashboard.css";
import UploadCard from "../../components/UploadCard/UploadCard";

function Dashboard() {

  return (
    <div className="dashboard">

      <header className="header">
        <h1>🎙️ AcousticSpace</h1>
        <p>AI Powered Deepfake Audio Detection</p>
      </header>

      <UploadCard />

    </div>
  );
}

export default Dashboard;