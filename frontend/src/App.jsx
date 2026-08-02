import { useState } from "react";
import Navbar from "./components/Navbar/Navbar";
import Dashboard from "./pages/Dashboard/Dashboard";
import History from "./components/History/History";
import "./App.css";

function App() {

  const [showHistory, setShowHistory] = useState(false);

  const [history, setHistory] = useState(() => {
    const savedHistory = localStorage.getItem("analysisHistory");

    return savedHistory
      ? JSON.parse(savedHistory)
      : [];
  });

  const addToHistory = (result, fileName) => {

    const newHistoryItem = {
      fileName,
      prediction: result.prediction,
      confidence_score: result.confidence_score,
      date: new Date().toLocaleString()
    };

    const updatedHistory = [
      newHistoryItem,
      ...history
    ];

    setHistory(updatedHistory);

    localStorage.setItem(
      "analysisHistory",
      JSON.stringify(updatedHistory)
    );
  };

  const clearHistory = () => {
    setHistory([]);
    localStorage.removeItem("analysisHistory");
  };

  return (
    <>
      <Navbar
        onHistoryClick={() => setShowHistory(true)}
      />

      <Dashboard
        onAnalysisComplete={addToHistory}
      />

      {/* Dark overlay */}
      {showHistory && (
        <div
          className="history-overlay"
          onClick={() => setShowHistory(false)}
        />
      )}

      {/* History Sidebar */}
      <aside
        className={`history-sidebar ${
          showHistory ? "open" : ""
        }`}
      >

        <div className="history-sidebar-header">

          <h2>Analysis History</h2>

          <button
            className="close-history"
            onClick={() => setShowHistory(false)}
          >
            ✕
          </button>

        </div>

        <History
          history={history}
          onClearHistory={clearHistory}
        />

      </aside>

    </>
  );
}

export default App;