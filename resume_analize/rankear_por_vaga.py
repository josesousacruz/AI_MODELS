from sentence_transformers import SentenceTransformer, util
from pathlib import Path

import json

def ranquear_curriculos_por_vaga(caminho_json, descricao_vaga, top_n=10):
    with open(caminho_json, "r", encoding="utf-8") as f:
        curriculos = json.load(f)

    modelo = SentenceTransformer("paraphrase-MiniLM-L6-v2")

    emb_vaga = modelo.encode(descricao_vaga, convert_to_tensor=True)
    textos = list(curriculos.values())
    caminhos = list(curriculos.keys())

    emb_curriculos = modelo.encode(textos, convert_to_tensor=True)

    similaridades = util.cos_sim(emb_vaga, emb_curriculos)[0]

    ranking = sorted(zip(caminhos, similaridades.tolist()), key=lambda x: x[1], reverse=True)

    print(f"\n Top {top_n} currículos mais compatíveis:")
    for i, (caminho, score) in enumerate(ranking[:top_n], 1):
        # Ao exibir o resultado:
        score_porcentagem = score * 100
        print(f"{i:02d}. Compatibilidade: {score_porcentagem:.2f}% | {Path(caminho).name}")


    return ranking

