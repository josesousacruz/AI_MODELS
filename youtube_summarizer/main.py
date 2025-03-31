from download_audio import download_audio
from transcribe_audio import transcribe_audio
from summarize import summarize_text
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from textwrap import wrap
import re

def main():
    url = "https://www.youtube.com/watch?v=69l-iaw_Vz0"
    print("Baixando áudio...")
    yt,audio_path = download_audio(url)
    
    print("Transcrevendo áudio...")
    transcription = transcribe_audio(audio_path)
    
    print("Gerando resumo com Gemini...")
    summary = summarize_text(transcription)
    
    # Gerar nome do arquivo com título do vídeo
    title = yt.title
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    pdf_filename = f"{safe_title}.pdf"
    
    md_filename = f"{safe_title}.md"
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(summary)

    # Cria o PDF
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    width, height = A4
    textobject = c.beginText(40, height - 50)
    textobject.setFont("Helvetica", 12)

    # Quebra o texto em linhas ajustadas à largura da página
    for paragraph in summary.split("\n"):
        wrapped_lines = wrap(paragraph, width=90)
        for line in wrapped_lines:
            textobject.textLine(line)
        textobject.textLine("")  # quebra entre parágrafos

    c.drawText(textobject)
    c.save()

    print(f"\n✅ PDF gerado com sucesso: {pdf_filename}")


if __name__ == "__main__":
    main()
