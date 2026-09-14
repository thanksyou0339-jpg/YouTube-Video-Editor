FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    fonts-dejavu \
    fonts-noto-core \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p output temp uploads

ENV PORT=5000

EXPOSE 5000

CMD ["python", "app.py"]
