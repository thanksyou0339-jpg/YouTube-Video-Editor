let mediaRecorder = null;
let recordedChunks = [];


async function generateVideo() {

    const button =
        document.getElementById("generateBtn");

    const status =
        document.getElementById("status");


    const topic =
        document.getElementById("topic").value.trim();

    const arabic =
        document.getElementById("arabic").value.trim();

    const translation =
        document.getElementById("translation").value.trim();

    const explanation =
        document.getElementById("explanation").value.trim();

    const voice =
        document.getElementById("voice").value;

    const background =
        document.getElementById("background").value.trim();


    if (!arabic && !translation && !explanation) {

        status.innerText =
            "براہ کرم حدیث، ترجمہ یا وضاحت درج کریں۔";

        return;
    }


    button.disabled = true;

    button.innerText =
        "⏳ ویڈیو تیار ہو رہی ہے...";

    status.innerText =
        "براہ کرم انتظار کریں، ویڈیو بنائی جا رہی ہے۔";


    try {

        const response =
            await fetch("/generate", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    topic: topic,

                    arabic: arabic,

                    translation: translation,

                    explanation: explanation,

                    voice: voice,

                    background: background

                })

            });


        const data =
            await response.json();


        if (!data.success) {

            throw new Error(
                data.error ||
                "Video generation failed"
            );

        }


        const video =
            document.getElementById(
                "videoPreview"
            );

        const resultCard =
            document.getElementById(
                "resultCard"
            );

        const download =
            document.getElementById(
                "downloadBtn"
            );


        video.src =
            data.video;

        download.href =
            data.video;


        resultCard.style.display =
            "block";


        status.innerText =
            "✅ ویڈیو کامیابی سے تیار ہو گئی۔";


        resultCard.scrollIntoView({
            behavior: "smooth"
        });


    } catch (error) {

        console.error(error);

        status.innerText =
            "❌ مسئلہ: " +
            error.message;

    } finally {

        button.disabled = false;

        button.innerText =
            "🎬 ویڈیو بنائیں";
    }
}



async function startRecording() {

    const video =
        document.getElementById(
            "videoPreview"
        );

    const status =
        document.getElementById(
            "recordStatus"
        );


    if (!video.src) {

        status.innerText =
            "پہلے ویڈیو تیار کریں۔";

        return;
    }


    try {

        await video.play();

    } catch (e) {

        status.innerText =
            "پہلے ویڈیو کے Play بٹن کو دبائیں۔";

        return;
    }


    const stream =
        video.captureStream
            ? video.captureStream()
            : video.mozCaptureStream();


    if (!stream) {

        status.innerText =
            "اس Browser میں Screen/Video recording support دستیاب نہیں۔";

        return;
    }


    recordedChunks = [];


    mediaRecorder =
        new MediaRecorder(
            stream,
            {
                mimeType:
                    "video/webm"
            }
        );


    mediaRecorder.ondataavailable =
        function(event) {

            if (event.data.size > 0) {

                recordedChunks.push(
                    event.data
                );

            }

        };


    mediaRecorder.onstop =
        function() {

            const blob =
                new Blob(
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


            a.click();


            status.innerText =
                "✅ Recording محفوظ ہو گئی۔";

        };


    mediaRecorder.start();


    status.innerText =
        "🔴 Recording جاری ہے...";


    video.onended =
        function() {

            if (
                mediaRecorder &&
                mediaRecorder.state !== "inactive"
            ) {

                mediaRecorder.stop();

            }

        };
}



function stopRecording() {

    if (
        mediaRecorder &&
        mediaRecorder.state !== "inactive"
    ) {

        mediaRecorder.stop();

    }

}
