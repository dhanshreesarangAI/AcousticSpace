import { useEffect, useState } from "react";
import "./Waveform.css";

function Waveform({ audioURL }) {

    const [progress, setProgress] = useState(0);

    useEffect(() => {

        const audio = document.getElementById("audio-player");

        if (!audio) return;

        const handleTimeUpdate = () => {

            if (audio.duration) {
                const percentage =
                    (audio.currentTime / audio.duration) * 100;

                setProgress(percentage);
            }
        };

        const handleEnded = () => {
            setProgress(100);
        };

        const handleLoaded = () => {
            setProgress(0);
        };

        audio.addEventListener("timeupdate", handleTimeUpdate);
        audio.addEventListener("ended", handleEnded);
        audio.addEventListener("loadedmetadata", handleLoaded);

        return () => {
            audio.removeEventListener(
                "timeupdate",
                handleTimeUpdate
            );

            audio.removeEventListener(
                "ended",
                handleEnded
            );

            audio.removeEventListener(
                "loadedmetadata",
                handleLoaded
            );
        };

    }, [audioURL]);

    const bars = [
        35, 55, 75, 45, 90, 60,
        40, 80, 50, 70, 95, 55,
        35, 65, 85, 45, 75, 50,
        90, 60, 40, 70, 85, 55
    ];

    return (
        <div className="waveform">

            <div
                className="wave-progress"
                style={{
                    width: `${progress}%`
                }}
            />

            <div className="wave-bars">

                {bars.map((height, index) => (
                    <div
                        key={index}
                        className="wave-bar"
                        style={{
                            height: `${height}%`
                        }}
                    />
                ))}

            </div>

        </div>
    );
}

export default Waveform;