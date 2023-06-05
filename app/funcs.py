from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pathlib
import smtplib
import random


def senha(email):
    itens = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            
    codigo = ''.join(random.choice(itens) for i in range(30))

    EMAIL_ADDRESS = "softmaze6@gmail.com"
    EMAIL_PASSWORD = "rilfivkrcwbpenpy"

    link = f"http://127.0.0.1:5011/revalidacao/senha/{codigo}"

    me = EMAIL_ADDRESS
    you = email

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Recuperação de senha - Knowzone"
    msg['From'] = me
    msg['To'] = you

    html = f"""\
        <!DOCTYPE html>
        <html>
        <head>
                  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                  <title>KEYS | Informativo</title>
                  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                  <link rel="preconnect" href="https://fonts.googleapis.com">
                  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
                  <link rel="preconnect" href="https://fonts.googleapis.com">
                  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap" rel="stylesheet">
        </head>

        <body>

                <nav>
                        <div class="logo">
                                <h1>Olá, { email } |</h1>
                        </div>
                </nav>

                <div class="msg">
                        <p>Olá, você recebeu este email porque</p>
                        <p>deseja recuperar a senha de sua conta .</p>
                        <p>Clique no link a seguir e troque a senha sua senha .</p>
                        <p>-</p>
                        <p>-</p>
                        <p>Link: {link}</p>
                </div>

                <div class="info">
                        <p>Email: { email }</p>
                </div>

                <footer>
                        <p> © 2023 Knowzone</p>
                </footer>

        </body>
        </html>
    """
        
    part1 = MIMEText(html, 'html')

    msg.attach(part1)

    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login(me, EMAIL_PASSWORD)
    mail.sendmail(me, you, msg.as_string())
    mail.quit()
