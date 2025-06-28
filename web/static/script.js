const recordBtn = document.getElementById("recordBtn");
const questionEl = document.getElementById("question");
const transcriptEl = document.getElementById("transcript");
const statusEl = document.getElementById("status");

let mediaRecorder;
let audioChunks = [];

// Load first question on page load
window.onload = () => {
    askNextQuestion("");  // triggers "What is your name?" if not yet asked
};

// 🎤 Start recording
recordBtn.addEventListener("click", async () => {
    if (!navigator.mediaDevices) {
        alert("Your browser does not support audio recording.");
        return;
    }

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const source = audioContext.createMediaStreamSource(stream);
    const analyser = audioContext.createAnalyser();
    source.connect(analyser);
    analyser.fftSize = 2048;

    const bufferLength = analyser.fftSize;
    const dataArray = new Uint8Array(bufferLength);

    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = event => {
        if (event.data.size > 0) {
            audioChunks.push(event.data);
        }
    };

    mediaRecorder.onstop = async () => {
        audioContext.close();
        updateStatus("🔄 Transcribing...");

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
                updateStatus("✅ Response received.");
                askNextQuestion(result.transcript);
            } else {
                transcriptEl.textContent = "⚠️ Transcription failed.";
                updateStatus("❌ Transcription failed.");
            }
        } catch (err) {
            console.error("❌ Error transcribing audio:", err);
            transcriptEl.textContent = "⚠️ Transcription error.";
            updateStatus("❌ Transcription error.");
        }
    };

    mediaRecorder.start();
    updateStatus("🎙️ Listening...");
    recordBtn.textContent = "⏹️ Stop Recording";
    recordBtn.onclick = stopRecording;

    // 🔇 Silence detection
    let silenceStart = null;
    const silenceThreshold = 2.5; // seconds of silence before stopping
    const checkInterval = 100;    // ms between checks

    function detectSilence() {
        analyser.getByteTimeDomainData(dataArray);

        // Compute RMS (volume level)
        let sum = 0;
        for (let i = 0; i < bufferLength; i++) {
            const normalized = (dataArray[i] - 128) / 128;
            sum += normalized * normalized;
        }
        const rms = Math.sqrt(sum / bufferLength);

        if (rms < 0.01) {
            if (silenceStart === null) {
                silenceStart = Date.now();
            } else {
                const elapsed = (Date.now() - silenceStart) / 1000;
                if (elapsed >= silenceThreshold) {
                    console.log("🤫 Silence detected — auto-stopping recording.");
                    stopRecording();
                    return;
                }
            }
        } else {
            silenceStart = null;
        }

        if (mediaRecorder && mediaRecorder.state === "recording") {
            setTimeout(detectSilence, checkInterval);
        }
    }

    detectSilence();
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
    updateStatus("🧠 Thinking...");
    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ last_response: lastTranscript })
        });

        const result = await res.json();

        // if (result.done) {
        //     questionEl.textContent = "✅ Interview complete!";
        //     speakText("Thank you. The interview is complete.");
        //     updateStatus("🎉 Interview complete!");
        //     return;
        // }
        if (result.done) {
            questionEl.textContent = "✅ Interview complete!";
            speakText("Thank you. The interview is complete.");
            updateStatus("🎉 Interview complete!");

            if (result.summary) {
                showSummary(result.summary);
            }
            return;
        }


        questionEl.textContent = "🤖 " + result.question;
        updateStatus("🔊 Speaking...");
        speakText(result.question);

    } catch (err) {
        console.error("❌ Error getting next question:", err);
        questionEl.textContent = "⚠️ Failed to get question.";
        updateStatus("❌ Failed to get next question.");
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

    utter.onend = () => {
        updateStatus("");  // Clear status when speaking finishes
    };
}

// 🛎️ Status helper
function updateStatus(message) {
    statusEl.textContent = message;
    if (message) {
        setTimeout(() => {
            if (statusEl.textContent === message) {
                statusEl.textContent = "";
            }
        }, 4000);
    }
}

function showSummary(summary) {
    let summaryHtml = "<h3>📋 Interview Summary:</h3><ul>";
    for (const [question, answer] of Object.entries(summary)) {
        summaryHtml += `<li><strong>${question}:</strong> ${answer || "(No answer)"} </li>`;
    }
    summaryHtml += "</ul>";
    document.getElementById("transcript").innerHTML = summaryHtml;
}