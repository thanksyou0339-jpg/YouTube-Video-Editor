import os
import subprocess
import requests
import textwrap

from PIL import Image, ImageDraw, ImageFont

from voice_generator import generate_voice


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)


WIDTH = 1920
HEIGHT = 1080


def get_font(size=48):
    possible_fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansArabic-Regular.ttf"
    ]

    for font in possible_fonts:
        if os.path.exists(font):
            return ImageFont.truetype(font, size)

    return ImageFont.load_default()


def download_background(url, filename):
    if not url:
        return None

    try:
        response = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        with open(filename, "wb") as f:
            f.write(response.content)

        return filename

    except Exception as e:
        print("Background download failed:", e)
        return None


def create_slide(
    filename,
    topic,
    arabic,
    translation,
    explanation,
    background_path=None
):
    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        (20, 20, 20)
    )

    if background_path and os.path.exists(background_path):
        try:
            bg = Image.open(background_path).convert("RGB")
            bg = bg.resize((WIDTH, HEIGHT))
            image.paste(bg)
        except Exception:
            pass

    draw = ImageDraw.Draw(image)

    # Dark overlay
    overlay = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 145)
    )

    image = Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    ).convert("RGB")

    draw = ImageDraw.Draw(image)

    title_font = get_font(60)
    arabic_font = get_font(62)
    translation_font = get_font(48)
    explanation_font = get_font(42)
    small_font = get_font(32)

    # Title
    if topic:
        draw.text(
            (WIDTH // 2, 80),
            topic,
            font=title_font,
            fill="white",
            anchor="ma"
        )

    y = 230

    # Arabic
    if arabic:
        arabic_lines = textwrap.wrap(
            arabic,
            width=42
        )

        for line in arabic_lines[:6]:
            draw.text(
                (WIDTH // 2, y),
                line,
                font=arabic_font,
                fill="white",
                anchor="ma"
            )
            y += 90

    y += 40

    # Translation
    if translation:
        draw.text(
            (WIDTH // 2, y),
            "ترجمہ",
            font=small_font,
            fill="white",
            anchor="ma"
        )

        y += 60

        translation_lines = textwrap.wrap(
            translation,
            width=55
        )

        for line in translation_lines[:6]:
            draw.text(
                (WIDTH // 2, y),
                line,
                font=translation_font,
                fill="white",
                anchor="ma"
            )
            y += 65

    y += 35

    # Explanation
    if explanation:
        explanation_lines = textwrap.wrap(
            explanation,
            width=65
        )

        for line in explanation_lines[:5]:
            draw.text(
                (WIDTH // 2, y),
                line,
                font=explanation_font,
                fill="white",
                anchor="ma"
            )
            y += 55

    # Footer
    draw.text(
        (WIDTH // 2, HEIGHT - 60),
        "اسلامی معلومات — مستند حوالہ ضرور چیک کریں",
        font=small_font,
        fill="white",
        anchor="mm"
    )

    image.save(filename, quality=95)


def get_audio_duration(filename):
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        filename
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    try:
        return float(result.stdout.strip())
    except Exception:
        return 10


def create_video(
    video_id,
    topic,
    arabic,
    translation,
    explanation,
    voice,
    background_url=None
):

    work_dir = os.path.join(
        TEMP_DIR,
        video_id
    )

    os.makedirs(work_dir, exist_ok=True)

    background_path = os.path.join(
        work_dir,
        "background.jpg"
    )

    if background_url:
        download_background(
            background_url,
            background_path
        )

    # Full narration
    full_text = ""

    if arabic:
        full_text += arabic + "\n\n"

    if translation:
        full_text += translation + "\n\n"

    if explanation:
        full_text += explanation

    audio_file = os.path.join(
        work_dir,
        "voice.mp3"
    )

    generate_voice(
        text=full_text,
        voice=voice,
        output_file=audio_file
    )

    duration = get_audio_duration(audio_file)

    slide_file = os.path.join(
        work_dir,
        "slide.jpg"
    )

    create_slide(
        filename=slide_file,
        topic=topic,
        arabic=arabic,
        translation=translation,
        explanation=explanation,
        background_path=background_path
    )

    output_filename = f"{video_id}.mp4"

    output_path = os.path.join(
        OUTPUT_DIR,
        output_filename
    )

    command = [
        "ffmpeg",
        "-y",

        "-loop",
        "1",

        "-i",
        slide_file,

        "-i",
        audio_file,

        "-t",
        str(duration),

        "-vf",
        "scale=1920:1080,format=yuv420p",

        "-c:v",
        "libx264",

        "-preset",
        "medium",

        "-crf",
        "23",

        "-c:a",
        "aac",

        "-b:a",
        "192k",

        "-shortest",

        output_path
    ]

    subprocess.run(
        command,
        check=True
    )

    return output_filename
