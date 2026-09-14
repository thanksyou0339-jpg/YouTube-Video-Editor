import os
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory

from video_generator import create_video

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()

        topic = data.get("topic", "").strip()
        arabic = data.get("arabic", "").strip()
        translation = data.get("translation", "").strip()
        explanation = data.get("explanation", "").strip()

        voice = data.get("voice", "ur-PK-AsadNeural")
        background = data.get("background", "").strip()

        if not arabic and not translation and not explanation:
            return jsonify({
                "success": False,
                "error": "براہ کرم حدیث، ترجمہ یا وضاحت میں سے کچھ ضرور لکھیں۔"
            }), 400

        video_id = str(uuid.uuid4())

        result = create_video(
            video_id=video_id,
            topic=topic,
            arabic=arabic,
            translation=translation,
            explanation=explanation,
            voice=voice,
            background_url=background
        )

        return jsonify({
            "success": True,
            "video": f"/output/{result}"
        })

    except Exception as e:
        print("ERROR:", e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/output/<filename>")
def output_file(filename):
    return send_from_directory(OUTPUT_DIR, filename)


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "app": "Islamic Video Maker"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
