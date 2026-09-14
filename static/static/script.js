let mediaRecorder = null;
let recordedChunks = [];


async function generateVideo() {

    const hadith = document.getElementById("hadith").value.trim();
    const translation = document.getElementById("translation").value.trim();
    const explanation = document.getElementById("explanation").value.trim();
    const voice = document.getElementById("voice").value;
    const background = document.getElementById("background").value.trim();

    const status = document.getElementById("status");
    const resultSection = document.getElementById("resultSection");
    const videoPreview = document.getElementById("videoPreview");
    const downloadBtn = document.getElementById("downloadBtn");
    const generateBtn = document.getElementById("generateBtn");


    if (!hadith && !translation && !explanation) {

        status.innerText = "⚠️ براہِ کرم حدیث یا متن ضرور لکھیں۔";

        return;
    }


    generateBtn.disabled = true;
    generateBtn.innerText = "⏳ ویڈیو بن رہی ہے...";
    status.innerText = "⏳ براہِ کرم انتظار کریں، ویڈیو تیار کی جا رہی ہے...";
    resultSection.style.display = "none";


    try {

        const response = await fetch("/generate", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                hadith: hadith,
                translation: translation,
                explanation: explanation,
                voice: voice,
                background: background

            })

        });


        const data = await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.error || "ویڈیو بنانے میں مسئلہ پیش آیا۔"
            );

        }


        videoPreview.src = data.video_url;

        downloadBtn.href = data.video_url;

        downloadBtn.download = "islamic-video.mp4";


        resultSection.style.display = "block";

        status.innerText = "✅ ویڈیو کامیابی سے تیار ہو گئی۔";


        resultSection.scrollIntoView({

            behavior: "smooth"

        });


    } catch (error) {

        console.error(error);

        status.innerText =
            "❌ مسئلہ: " + error.message;

    } finally {

        generateBtn.disabled = false;

        generateBtn.innerText = "🎬 ویڈیو بنائیں";

    }

}



async function startRecording() {

    const video = document.getElementById("videoPreview");

    const recordingStatus =
        document.getElementById("recordingStatus");


    if (!video.src) {

        recordingStatus.innerText =
            "⚠️ پہلے ویڈیو تیار کریں۔";

        return;

    }


    try {

        const stream = video.captureStream();

        recordedChunks = [];


        mediaRecorder = new MediaRecorder(

            stream,

            {
                mimeType: "video/webm"
            }

        );


        mediaRecorder.ondataavailable = function(event) {

            if (event.data.size > 0) {

                recordedChunks.push(event.data);

            }

        };


        mediaRecorder.onstop = function() {

            const blob = new Blob(

                recordedChunks,

                {
                    type: "video/webm"
                }

            );


            const url =
                URL.createObjectURL(blob);


            const a =
                document.createElement("a");


            a.href = url;

            a.download =
                "islamic-video-recording.webm";


            document.body.appendChild(a);

            a.click();

            document.body.removeChild(a);


            URL.revokeObjectURL(url);


            recordingStatus.innerText =
                "✅ Recording محفوظ ہو گئی۔";

        };


        mediaRecorder.start();


        video.play();


        recordingStatus.innerText =
            "🔴 Recording شروع ہو گئی...";


    } catch (error) {

        console.error(error);

        recordingStatus.innerText =
            "❌ Recording شروع نہیں ہو سکی۔";

    }

}



function stopRecording() {

    if (
        mediaRecorder &&
        mediaRecorder.state !== "inactive"
    ) {

        mediaRecorder.stop();

    } else {

        document.getElementById(
            "recordingStatus"
        ).innerText =
            "⚠️ ابھی کوئی recording نہیں چل رہی۔";

    }

}
