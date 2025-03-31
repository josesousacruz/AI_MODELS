import google.generativeai as genai

# Coloque sua chave da API do Gemini
genai.configure(api_key="AIzaSyCO_msZsPISAXoIqWEdN_7JMQcAx3SVcCg")

def summarize_text(text: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = (
    "Você é um jornalista experiente. A seguir está a transcrição de um vídeo do YouTube. "
    "Escreva um resumo completo e bem estruturado, em português"
    "Escreva tudo em markdown"
    "Use uma linguagem formal, clara e abrangente. Evite omissões.\n\n"
    f"Transcrição:\n{text}"
)
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"# Erro ao gerar resumo\n\n```\n{str(e)}\n```"
