import whisper

def transcribe_audio(audio_path: str) -> str:
    model = whisper.load_model("small")  # ou "small", "medium", etc.
    result = model.transcribe(audio_path)
    return result["text"]
