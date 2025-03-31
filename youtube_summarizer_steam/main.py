from stream_transcriber import stream_audio_to_whisper
from summarize import summarize_text
from generate_pdf import save_summary_as_pdf

def main():
    url = "https://www.youtube.com/watch?v=DNcdDHB8McE"

    print("🚀 Iniciando processo hardcore...")

    transcription, title = stream_audio_to_whisper(url)

    print("📄 Transcrição concluída. Gerando resumo...")
    summary = summarize_text(transcription)

    print("🖨️ Salvando PDF com título do vídeo...")
    save_summary_as_pdf(summary, title)

    print("✅ Finalizado com sucesso!")

if __name__ == "__main__":
    main()
