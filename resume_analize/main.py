from pathlib import Path
from extrair_texto_curriculos import extrair_curriculos_das_pastas 
from email_utils import enviar_email_ranking
from rankear_por_vaga import ranquear_curriculos_por_vaga

PASTA_CVS = "data/INFORMATION-TECHNOLOGY"
ARQUIVO_SAIDA = "outputs/textos_extraidos.json"

DESCRICAO_VAGA = """A Truckpag busca Backend PHP/Laravel (pleno) para compor seu time!

A TruckPag, startup de Meios de Pagamento está em busca de profissionais que queiram causar impacto relevante no mundo, solucionar grandes problemas e tornar operações logísticas mais efetivas, mais assertivas e mais competitivas. Entendemos que grandes ideias nascem de vivências, formações e pessoas únicas, que gostam de trabalhar em um ambiente de colaboração, alta performance e descontraído, para agregar a nossa equipe.

Responsabilidades:

- Implementar e otimizar funcionalidades complexas no backend com PHP e Laravel

- Identificar e corrigir bugs e problemas de performance, garantindo a manutenção de sistemas existentes

- Criar e documentar APIs RESTful para integrações com sistemas internos e externos

- Participar de reuniões de planejamento e colaborar com equipes de frontend, design e produto

- Escrever testes unitários e de integração para assegurar a qualidade e estabilidade do código

- Realizar modelagem de dados e otimizar queries para eficiência e escalabilidade

- Documentar código e processos, e propor melhorias para o sistema e fluxo de trabalho

A Truckpag busca Backend PHP/Laravel (pleno) para compor seu time!

A TruckPag, startup de Meios de Pagamento está em busca de profissionais que queiram causar impacto relevante no mundo, solucionar grandes problemas e tornar operações logísticas mais efetivas, mais assertivas e mais competitivas. Entendemos que grandes ideias nascem de vivências, formações e pessoas únicas, que gostam de trabalhar em um ambiente de colaboração, alta performance e descontraído, para agregar a nossa equipe.

Responsabilidades:

- Implementar e otimizar funcionalidades complexas no backend com PHP e Laravel

- Identificar e corrigir bugs e problemas de performance, garantindo a manutenção de sistemas existentes

- Criar e documentar APIs RESTful para integrações com sistemas internos e externos

- Participar de reuniões de planejamento e colaborar com equipes de frontend, design e produto

- Escrever testes unitários e de integração para assegurar a qualidade e estabilidade do código

- Realizar modelagem de dados e otimizar queries para eficiência e escalabilidade

- Documentar código e processos, e propor melhorias para o sistema e fluxo de trabalho

Habilidades
PHP, Laravel, PHPUnit, GIT, SQL, DOCKER, REST API
"""

def main():
    print(f"Caminho absoluto da pasta: {Path(PASTA_CVS).resolve()}")
    print(f"\nLendo currículos da pasta: {PASTA_CVS}")
    extrair_curriculos_das_pastas(PASTA_CVS, ARQUIVO_SAIDA)
    print(" Processo finalizado.")
    
    print("\n Iniciando ranqueamento por compatibilidade com a vaga...")
    ranking = ranquear_curriculos_por_vaga(ARQUIVO_SAIDA, DESCRICAO_VAGA)

    # Informações para envio do email
    email_destino = "emaildestino@gmail.com"
    email_remetente = "emailremetente@gmail.com.br"
    senha_remetente = "vnmfpbxtsvvfrdsn"  # recomendo usar uma senha de app
    smtp_server="smtp.office365.com" #utilize o smtp_Server que preferir
    smtp_port=587

    enviar_email_ranking(
        ranking, 
        email_destino, 
        email_remetente, 
        senha_remetente,
        smtp_server,
        smtp_port
    )

if __name__ == "__main__":
    main()

