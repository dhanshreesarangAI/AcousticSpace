import "./History.css";

function History({ history, onClearHistory }) {
    if (!history || history.length === 0) {
        return (
            <div className="history-card">
                <div className="history-header">
                    <h2>Analysis History</h2>
                </div>

                <p className="empty-history">
                    No analysis history yet.
                </p>
            </div>
        );
    }

    return (
        <div className="history-card">

            <div className="history-header">
                <h2>Analysis History</h2>

                <button onClick={onClearHistory}>
                    Clear History
                </button>
            </div>

            <div className="history-list">

                {history.map((item, index) => {

                    const predictionClass =
                        item.prediction === "REAL" ? "green" : "red";

                    return (
                        <div className="history-item" key={index}>

                            <div className="history-file">
                                <strong>{item.fileName}</strong>
                                <span>{item.date}</span>
                            </div>

                            <div
                                className={`history-prediction ${predictionClass}`}
                            >
                                {item.prediction}
                            </div>

                            <div className="history-confidence">
                                {item.confidence_score}%
                            </div>

                        </div>
                    );
                })}

            </div>

        </div>
    );
}

export default History;