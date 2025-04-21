
from flask import Flask, render_template, request, send_file, redirect, url_for
import yt_dlp
import os
import uuid
from moviepy.editor import VideoFileClip
import random

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Lista de vídeos engraçados (poderia ser dinamicamente buscada)
FUNNY_VIDEOS = [
    "https://www.youtube.com/watch?v=8ybW48rKBME",
    "https://www.youtube.com/watch?v=MtN1YnoL46Q",
    "https://www.youtube.com/watch?v=j5a0jTc9S10"
]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/random')
def random_video():
    return render_template("index.html", random_url=random.choice(FUNNY_VIDEOS))

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['url']
    video_id = str(uuid.uuid4())
    filename = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")
    clipped_filename = os.path.join(DOWNLOAD_DIR, f"{video_id}_clipped.mp4")

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': filename,
        'quiet': True,
        'merge_output_format': 'mp4',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    try:
        clip = VideoFileClip(filename).subclip(0, 90)
        clip.write_videofile(clipped_filename, codec="libx264", audio_codec="aac", logger=None)
        clip.close()
        os.remove(filename)
        return send_file(clipped_filename, as_attachment=True)
    except Exception as e:
        return f"Erro ao cortar vídeo: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
