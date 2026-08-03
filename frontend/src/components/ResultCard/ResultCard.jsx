import "./ResultCard.css";

function ResultCard({ result }) {

    const predictionClass =
        result.prediction === "REAL" ? "green" : "red";

    return (

        <div className={`result-card ${predictionClass}`}>

            <h2>Analysis Result</h2>

            <p>
                Prediction:
                <strong>
                    {result.prediction}
                </strong>
            </p>

            <p>
                Confidence:
                {result.confidence_score}%
            </p>

            <p>
                RIR Mismatch:
                {result.rir_mismatch}
            </p>

            <p>
                Breathing:
                {result.breathing}
            </p>

        </div>

    );
}

export default ResultCard;