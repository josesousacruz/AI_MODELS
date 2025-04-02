import pdfplumber
from pathlib import Path
import json
import os
from tqdm import tqdm

def extrair_curriculos_das_pastas(pasta_raiz, caminho_saida_json="outputs/textos_extraidos.json"):
    pasta = Path(pasta_raiz)
    lista_pdfs = [f for f in pasta.rglob("*") if f.suffix.lower() == ".pdf"]

    print(f" Procurando PDFs em: {Path(pasta_raiz).resolve()}")
    print(f" Total de arquivos PDF encontrados: {len(lista_pdfs)}\n")

    # Carregar dados anteriores se já existirem
    if os.path.exists(caminho_saida_json) and os.path.getsize(caminho_saida_json) > 0:
        with open(caminho_saida_json, "r", encoding="utf-8") as f:
            curriculos_extraidos = json.load(f)
    else:
        curriculos_extraidos = {}

    total_processados = 0
    total_novos = 0

    for caminho_pdf in tqdm(lista_pdfs, desc=" Processando PDFs"):
        caminho_str = str(caminho_pdf)
        total_processados += 1

        # Pula se já foi processado antes
        if caminho_str in curriculos_extraidos:
            continue

        try:
            with pdfplumber.open(caminho_pdf) as pdf:
                texto = ""
                for pagina in pdf.pages:
                    texto_pagina = pagina.extract_text()
                    if texto_pagina:
                        texto += texto_pagina + "\n"

                if texto.strip():
                    curriculos_extraidos[caminho_str] = texto.strip()
                    total_novos += 1

                    # Salva no JSON imediatamente
                    os.makedirs(Path(caminho_saida_json).parent, exist_ok=True)
                    with open(caminho_saida_json, "w", encoding="utf-8") as f:
                        json.dump(curriculos_extraidos, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f" Erro em {caminho_pdf.name}: {e}")

    print(f"\nPDFs processados no total: {total_processados}")
    print(f" Novos currículos extraídos e salvos: {total_novos}")
