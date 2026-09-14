🕌 Islamic Video Maker

یہ ایک ویب بیسڈ Islamic Video Maker ہے جس میں آپ حدیث، اردو ترجمہ اور وضاحت ڈال کر ویڈیو تیار کر سکتے ہیں۔

✨ Features

- 📖 عربی حدیث شامل کرنا
- 🌙 اردو ترجمہ شامل کرنا
- 📝 حدیث کی وضاحت شامل کرنا
- 🎙️ اردو اور عربی AI Voice
- 🎬 MP4 ویڈیو بنانا
- ▶️ Browser میں Video Preview
- ⬇️ Video Download
- 🔴 Browser Screen Recording
- 📱 Mobile-friendly interface
- 🎨 Animated Card-style design

📁 Project Structure

YouTube-Video-Editor/
│
├── app.py
├── video_generator.py
├── voice_generator.py
├── requirements.txt
├── Dockerfile
├── .gitignore
├── .env.example
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js

💻 Local Installation

اپنے کمپیوٹر پر repository download یا clone کریں۔

پھر project folder کے اندر terminal کھولیں۔

1. Dependencies install کریں

pip install -r requirements.txt

2. Application چلائیں

python app.py

3. Browser میں کھولیں

http://localhost:5000

🐳 Docker

اگر Docker استعمال کرنا ہو:

docker build -t islamic-video-maker .

پھر:

docker run -p 5000:5000 islamic-video-maker

Browser میں:

http://localhost:5000

🎙️ Voice

یہ ابتدائی version Edge TTS استعمال کرتا ہے، اس لیے شروع میں ElevenLabs API Key ضروری نہیں ہے۔

بعد میں ElevenLabs یا کسی دوسرے professional voice provider کو بھی شامل کیا جا سکتا ہے۔

🎥 Video

ابتدائی version میں:

- حدیث
- اردو ترجمہ
- وضاحت
- Background
- Voice

کو ملا کر video تیار کی جاتی ہے۔

بعد کے versions میں مزید features شامل کیے جا سکتے ہیں:

- Multiple images
- Automatic Islamic backgrounds
- Animated subtitles
- Arabic text styling
- Urdu text styling
- Multiple scenes
- Background music
- Voice timing
- YouTube Shorts format
- 16:9 YouTube format
- 9:16 Shorts format
- Automatic MP4 conversion

⚠️ Important

حدیث کا عربی متن، ترجمہ اور حوالہ ہمیشہ معتبر اسلامی ماخذ سے verify کریں۔

AI سے خود سے حدیث یا حدیث کا حوالہ ایجاد نہ کروائیں۔

ویڈیو میں اپنا original educational explanation اور useful information شامل کرنا بہتر ہے۔

📜 License

یہ project personal/educational use کے لیے بنایا گیا ہے۔
