from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import whisper
import yt_dlp
import os
import uuid

app = FastAPI()

# Allow requests from Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = whisper.load_model("base")

@app.post("/transcribe")
async def transcribe(req: Request):
    data = await req.json()
    youtube_url = data.get("youtube_url")
    if not youtube_url:
        return {"error": "No YouTube URL provided"}

    # Generate unique filename
    filename = f"audio_{uuid.uuid4()}.mp3"

    # Download audio using yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
    except Exception as e:
        return {"error": f"Download failed: {str(e)}"}

    try:
        result = model.transcribe(filename)
        os.remove(filename)
        return {"text": result["text"]}
    except Exception as e:
        return {"error": f"Transcription failed: {str(e)}"}