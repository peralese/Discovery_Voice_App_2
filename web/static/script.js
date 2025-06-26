const recordBtn = document.getElementById("recordBtn");
const questionEl = document.getElementById("question");
const transcriptEl = document.getElementById("transcript");

let mediaRecorder;
let audioChunks = [];

// Load first question on page load
window.onload = () => {
    askNextQuestion("");  // triggers "What is your name?" if not asked yet
};

// 🎤 Start recording
recordBtn.addEventListener("click", async () => {
    if (!navigator.mediaDevices) {
        alert("Your browser does not support audio recording.");
        return;
    }

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    audioChunks = [];
    mediaRecorder.ondataavailable = event => {
        if (event.data.size > 0) {
            audioChunks.push(event.data);
        }
    };

    mediaRecorder.onstop = async () => {
        const blob = new Blob(audioChunks, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append("audio", blob);

        try {
            const res = await fetch("/transcribe", {
                method: "POST",
                body: formData
            });
            const result = await res.json();

            if (result.transcript) {
                console.log("📝 Transcript:", result.transcript);
                transcriptEl.textContent = `📝 You said: "${result.transcript}"`;
                askNextQuestion(result.transcript);
            } else {
                transcriptEl.textContent = "⚠️ Transcription failed.";
            }
        } catch (err) {
            console.error("❌ Error transcribing audio:", err);
            transcriptEl.textContent = "⚠️ Transcription error.";
        }
    };

    mediaRecorder.start();
    recordBtn.textContent = "⏹️ Stop Recording";
    recordBtn.onclick = stopRecording;
});

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        recordBtn.textContent = "🎙️ Record Response";
        recordBtn.onclick = startRecording;
    }
}

function startRecording() {
    recordBtn.click();  // re-trigger recording
}

// 🔁 Ask next question
async function askNextQuestion(lastTranscript) {
    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ last_response: lastTranscript })
        });

        const result = await res.json();

        if (result.done) {
            questionEl.textContent = "✅ Interview complete!";
            speakText("Thank you. The interview is complete.");
            return;
        }

        questionEl.textContent = "🤖 " + result.question;
        speakText(result.question);

    } catch (err) {
        console.error("❌ Error getting next question:", err);
        questionEl.textContent = "⚠️ Failed to get question.";
    }
}

// 🔊 Text-to-speech
function speakText(text) {
    const synth = window.speechSynthesis;
    if (!synth) return;

    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = "en-US";
    utter.rate = 1.0;
    synth.speak(utter);
}
