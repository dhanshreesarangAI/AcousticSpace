import { useState } from "react";
import { analyzeAudio } from "../../services/api";
import ResultCard from "../ResultCard/ResultCard";

function UploadCard() {

    const [selectedFile, setSelectedFile] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);


    const handleFileChange = (event) => {

        const file = event.target.files[0];

        if(file){
            setSelectedFile(file);
        }
    };


    const handleAnalyze = async () => {

        if(!selectedFile){
            alert("Please select an audio file");
            return;
        }


        try{

            setLoading(true);

            const response = await analyzeAudio(selectedFile);

            setResult(response);

        }
        catch(error){

            console.log(error);
            alert("Audio analysis failed");

        }
        finally{

            setLoading(false);

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


            <input
                type="file"
                accept=".mp3,.wav,.m4a"
                onChange={handleFileChange}
            />


            {
                selectedFile && (

                    <div className="file-info">

                        <p>
                            <strong>Selected File:</strong>
                        </p>

                        <p>
                            {selectedFile.name}
                        </p>

                    </div>

                )
            }


            <button 
                onClick={handleAnalyze}
                disabled={loading}
            >

                {
                    loading 
                    ? "Analyzing..."
                    : "Analyze Audio"
                }

            </button>


            {
                result && (

                    <ResultCard result={result}/>

                )
            }


        </div>

    );

}

export default UploadCard;