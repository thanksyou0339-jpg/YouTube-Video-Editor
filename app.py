import os
from flask import Flask, render_template, request, jsonify, send_from_directory

from video_generator import create_video


app = Flask(__name__)

# Required folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMP_DIR = os.path.join(BASE_DIR, "temp")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "message": "Islamic Video Maker is running"
    })


@app.route("/generate", methods=["POST"])
def generate():

    try:
        data = request.get_json(silent=True) or {}

        hadith = str(data.get("hadith", "")).strip()
        translation = str(data.get("translation", "")).strip()
        explanation = str(data.get("explanation", "")).strip()

        voice = str(
            data.get(
                "voice",
                "ur-PK-UzmaNeural"
            )
        ).strip()

        background = str(
            data.get("background", "")
        ).strip()


        if not hadith and not translation and not explanation:

            return jsonify({
                "success": False,
                "error": "براہِ کرم حدیث، ترجمہ یا وضاحت میں کچھ لکھیں۔"
            }), 400


        video_filename = create_video(

            hadith=hadith,

            translation=translation,

            explanation=explanation,

            voice=voice,

            background_url=background,

            output_dir=OUTPUT_DIR,

            temp_dir=TEMP_DIR

        )


        return jsonify({

            "success": True,

            "video_url": "/output/" + video_filename

        })


    except Exception as e:

        print("VIDEO GENERATION ERROR:")
        print(str(e))

        return jsonify({

            "success": False,

            "error": "ویڈیو بنانے میں مسئلہ آیا: " + str(e)

        }), 500



@app.route("/output/<path:filename>")
def output_file(filename):

    return send_from_directory(
        OUTPUT_DIR,
        filename,
        as_attachment=False
    )



if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
