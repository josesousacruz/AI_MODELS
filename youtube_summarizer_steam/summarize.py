import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyCO_msZsPISAXoIqWEdN_7JMQcAx3SVcCg")

def summarize_text(text: str) -> str:
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    prompt = (
        "Você é um jornalista experiente. Abaixo está a transcrição de um vídeo do YouTube.\n"
        "Crie um resumo **completo, detalhado e estruturado** em **formato Markdown**, com pelo menos 4 parágrafos. "
        "Use títulos e subtítulos se possível. Escreva em português com linguagem formal e clara.\n\n"
        f"Transcrição:\n{text}"
    )

    response = model.generate_content(prompt)
    return response.text
