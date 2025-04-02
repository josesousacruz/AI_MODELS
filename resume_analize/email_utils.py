# email_utils.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

def enviar_email_ranking(
    ranking, 
    email_destino, 
    email_remetente, 
    senha_remetente, 
    smtp_server="smtp.office365.com", 
    smtp_port=587,                     
    top_n=10
):
    assunto = " Ranking de Currículos"
    
    corpo_html = "<h2> Melhores de Currículos</h2><ol>"
    for caminho, score in ranking[:top_n]:
        score_porcentagem = score * 100  # conversão para porcentagem aqui
        nome_cv = Path(caminho).name
        corpo_html += f"<li><strong>{nome_cv}</strong> - Compatibilidade: {score_porcentagem:.2f}%</li>"
    corpo_html += "</ol>"

    msg = MIMEMultipart()
    msg['From'] = email_remetente
    msg['To'] = email_destino
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo_html, 'html'))

    try:
        servidor = smtplib.SMTP(smtp_server, smtp_port)
        servidor.starttls()
        servidor.login(email_remetente, senha_remetente)
        servidor.sendmail(email_remetente, email_destino, msg.as_string())
        print(f"E-mail enviado com sucesso para {email_destino}")
    except Exception as e:
        print(f"Falha ao enviar e-mail: {e}")
    finally:
        servidor.quit()
