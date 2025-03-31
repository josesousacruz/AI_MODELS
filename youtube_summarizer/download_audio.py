from pytubefix import YouTube
from pydub import AudioSegment
import os
from static_ffmpeg import add_paths  # <- novo import

# Faz o setup automático do ffmpeg portátil
add_paths()

def download_audio(url: str, output_dir: str = "youtube_summarizer/downloads") -> str:
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Baixa o áudio original
    downloaded_path = audio_stream.download(output_path=output_dir)

    # Converte pra .mp3 com pydub
    mp3_path = os.path.splitext(downloaded_path)[0] + ".mp3"
    audio = AudioSegment.from_file(downloaded_path)
    audio.export(mp3_path, format="mp3")

    os.remove(downloaded_path)
    return yt,mp3_path
