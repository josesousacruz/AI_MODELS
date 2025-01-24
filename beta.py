from flask import Flask, request, jsonify
import google.generativeai as genai
import json
from cachetools import TTLCache
from flask_cors import CORS

# Configurar a chave da API
genai.configure(api_key='SUA_ACHA_AQUI')

# Configuração do modelo
generation_config = {
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 500,  # Restringe o tamanho da resposta
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# Carregar base de conhecimento
with open("base_conhecimento.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

# Inicializar o Flask
app = Flask(__name__)
CORS(app)
# Contextos separados
system_description = (
    "O iBalanca é um sistema especializado em gerenciar pesagens de veiculos com ou sem carga. "
    "Ele permite que os usuários registrem, acompanhem e analisem dados de pesagem de forma eficiente. "
    "As principais funcionalidades incluem: cadastro de veículos, gerenciamento de clientes, geração de relatórios de pesagem, "
    "integração com balanças para pegar peso automatico."
)

task_guidelines = (
    "Para realizar tarefas no iBalanca, siga estas diretrizes: "
    "Use o menu principal para acessar as seções do sistema. "
    "Preencha todos os campos obrigatórios ao cadastrar dados. "
    "Consulte os relatórios para análises detalhadas. "
    "Para pesagem manual é necessario que um administrador faça a liberação."
    "Para realizar uma pesagem, clique no botão iniciar pesagem!"
    "So é possivel realizar pesagem do veiculo se estiver programano no iAgendamento" 
    "Para cancelar uma pesagem é necessario clicar no icon de lixeira que aparece ao passar o mause sobre o ticket listado"
    "Para cancelar um ticket ou pesagem, basta passar o mouse sobre o ticket em questão, clicar no icone de lixeira que irá aparecer todas as pesagens relacionadas ao ticket! Eschola a pesagem e clique para cancelar!"
    "Lembrando que não é possivel cancelar uma pesagem caso exista pesagens abertas após ela! "
    "As pesagens podem ser refeitas após ser canceladas. O ticket é cancelado após cancelar a ultima pesagem aberta"
    "A programção precisa ser feita apenas uma vez para cada OS. Não precisa fazer uma nova programação para pesar novamente"
    "Para editar um ticket basta clicar no icone de caneta que aparece quando passa o mouse por cima do ticket listado. Basta fazer as alterações e salvar."
    "Se após iniciar a pesagem e inserir a placa do veiculo, o motorista da viagem para aquela programação estiver divergente do que se encontra dirigindo o veiculo, basta alterar para o motorista correto"
    "É possivel alterar o tipo do produto caso ele seja diferente ao que está em carregamento"
    "As mensagens no whatsapp são enviadas automaticamente no grupo configurado. Caso a unidade seja setada para envio de mensagens no grupo"
    "Caso um veiculo entrou no terminal ou uma pesagem final foi realizada e não foi enviada automaticamente uma mensagem informativa no grupo, entrem em contato com a TI"
    )

similar_question_instructions = (
    "Sempre verifique perguntas similares na base de conhecimento antes de responder. "
    "Se encontrar uma correspondência relevante, use-a como base para a resposta."
    "Responda de forma natural como se fosse uma funcionaria com bastante tempo e que conhece cada detalhe do sistema"
    "Reponda de forma objetiva"
)

user_histories = TTLCache(maxsize=1000, ttl=1800)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Obter o input da requisição
        data = request.get_json()
        user_id = data.get('user_id')  # Identificador único do usuário
        user_message = data.get('message', '')

        # Verificar se a mensagem foi fornecida
        if not user_message:
            return jsonify({"error": "Nenhuma mensagem fornecida."}), 400
        
                # Verificar se user_id e message foram fornecidos
        if not user_id or not user_message:
            return jsonify({"error": "É necessário fornecer 'user_id' e 'message'."}), 400

        # Inicializar o histórico do usuário se não existir
        if user_id not in user_histories:
            user_histories[user_id] = []


        # Buscar informações na base de conhecimento
        response_from_kb = search_knowledge_base(user_message)

        if response_from_kb:
            # Atualizar o histórico com a interação
            user_histories[user_id].append({"role": "user", "parts": [user_message]})
            user_histories[user_id].append({"role": "model", "parts": [response_from_kb]})

            # Retornar a resposta da base de conhecimento
            return jsonify({"response": response_from_kb})

      # Criar uma sessão de chat com o histórico do usuário
        chat_session = model.start_chat(history=user_histories[user_id])

        # Montar o prompt final com os contextos fixos
        prompt = (
            f"{system_description}\n\n"
            f"{task_guidelines}\n\n"
            f"{similar_question_instructions}\n\n"
            f"Pergunta do usuário: {user_message}"
        )

        # Enviar a mensagem ao modelo
        response = chat_session.send_message(prompt)
        
        # Atualizar o histórico com a interação
        user_histories[user_id].append({"role": "user", "parts": [user_message]})
        user_histories[user_id].append({"role": "model", "parts": [response.text.strip()]})


        # Retornar a resposta processada
        return jsonify({"response": response.text.strip()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def search_knowledge_base(user_message):
    """
    Busca na base de conhecimento uma resposta para a mensagem do usuário com base em keywords.
    """
    user_message_lower = user_message.lower()
    for item in knowledge_base:
        # Verifica se a mensagem do usuário está na pergunta ou nas keywords
        if user_message_lower in item["question"].lower() or any(keyword in user_message_lower for keyword in item["keywords"]):
            return item["answer"]
    return None

if __name__ == '__main__':
    app.run(debug=True)
