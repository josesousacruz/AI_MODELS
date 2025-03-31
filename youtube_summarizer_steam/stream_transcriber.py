import subprocess
import whisper
from pytubefix import YouTube
import os
import tempfile
from static_ffmpeg import run

ffmpeg_path, _ = run.get_or_fetch_platform_executables_else_raise()
ffmpeg_dir = os.path.dirname(ffmpeg_path)
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]

def stream_audio_to_whisper(url):
    print("🔗 Preparando stream do YouTube...")

    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    stream_url = audio_stream.url

    print("🎧 Iniciando FFmpeg para capturar o áudio em tempo real...")

    # Pega os executáveis do static-ffmpeg
    ffmpeg_path, ffprobe_path = run.get_or_fetch_platform_executables_else_raise()

    # Cria um arquivo temporário para salvar o áudio convertido
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_audio_path = temp_audio.name
    temp_audio.close()

    # Comando FFmpeg para converter o áudio em stream
    ffmpeg_cmd = [
        ffmpeg_path,
        "-i", stream_url,
        "-f", "wav",
        "-ac", "1",
        "-ar", "16000",
        "-loglevel", "quiet",
        temp_audio_path
    ]

    subprocess.run(ffmpeg_cmd)

    print("🧠 Enviando stream para o Whisper...")
    model = whisper.load_model("base")
    result = model.transcribe(temp_audio_path)

    os.remove(temp_audio_path)

    return result["text"], yt.title
