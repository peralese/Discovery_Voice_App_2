let mediaRecorder;
let audioChunks = [];

function startInterview() {
  fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ last_response: "" })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("question-box").innerText = data.question;
  });
}

function startRecording() {
  navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
    mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });
    mediaRecorder.start();
    audioChunks = [];

    console.log("🎙️ Recording started...");

    mediaRecorder.ondataavailable = e => {
      audioChunks.push(e.data);
    };

    mediaRecorder.onstop = () => {
      const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
      document.getElementById("playback").src = URL.createObjectURL(audioBlob);

      const formData = new FormData();
      formData.append("audio", audioBlob, "response.webm");

      fetch("/transcribe", {
        method: "POST",
        body: formData
      })
      .then(res => {
        if (!res.ok) throw new Error(`Server error: ${res.status}`);
        return res.json();
      })
      .then(data => {
        document.getElementById("transcript").innerText = data.transcript;
        console.log("📝 Transcript:", data.transcript);
      })
      .catch(err => {
        console.error("❌ Error during transcription:", err);
        alert("Transcription failed. Check backend logs.");
      });
    };

    setTimeout(() => {
      mediaRecorder.stop();
      console.log("🛑 Recording stopped.");
    }, 8000); // 8 seconds max
  });
}
