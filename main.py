
'''

	Criado por: dcgo15 


'''


# O código principal

from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user, login_required
from app.models import *
from app import app, models
from email.mime.multipart import MIMEMultipart
from authlib.integrations.flask_client import OAuth
from email.mime.text import MIMEText
from pip._vendor import cachecontrol
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from apiclient.discovery import build
import pathlib
import smtplib
import random


# Chaves para Google

CLIENT_SECRETS_FILE = "client_secret_login.json"
CLIENT_SECRETS_FILE_sign_mentor = "client_secret_sign_mentor.json"
CLIENT_SECRETS_FILE_sign_estudante = "client_secret_sign_estudante.json"

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly openid',
          'https://www.googleapis.com/auth/userinfo.email openid',
          'https://www.googleapis.com/auth/userinfo.profile openid']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'



# Credenciais, conexao com o json 


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


# Aqui é uma das rotas, aqui ficará a landing page


@app.route("/")
def inicio():
    return render_template("site.html") 

# Passar o comando de pesquisa	

@app.route("/lobby")
def index():
    return render_template("index.html") 


@app.route("/nao_encontrada")
def error():
    return render_template("error.html")


# Recuperação e revalidação de senha

@app.route("/recuperacao/senha", methods=["GET", "POST"])
def recuperacao():

    if request.method=="POST":
        email = request.form["email"]
        session["email"] = email
    
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
    
    
    return render_template("recuperacao_senha.html")

@app.route("/revalidacao/senha/<codigo>", methods=["GET", "POST"])
def revalidacao(codigo):
    if "email" in session:
        email = session["email"]

        us = user.query.filter_by(email=email).first()

        if request.method=="POST":

            senha = request.form["senha"]
            
            if us is not None:
                us.senha = senha
                db.session.commit()
            else:
                flash('Email de usuário inexistente', 'error')


# Area dos formulários de login e sign

@app.route("/options", methods=["GET", "POST"])
def opcao_conta():
    if request.method == "POST":

       if request.form.get("study") == "Estudante":
               return redirect(url_for("signup_estudante"))

       elif request.form.get("admin") == "Admin":
               return redirect(url_for("signup_mentor"))

    return render_template("opcao.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
              
       em = request.form["email"]
       senha = request.form["senha"]

       us = user.query.filter_by(email=em, senha=senha).first()
                       
       if us is None:
            flash('Usuário inexistente ou dados incorretos', 'error')
                  
       else:

           session["nome"] = us.nome

           login_user(us)

           return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/nova_conta/estudante", methods=["GET", "POST"])
def signup_estudante():
    if request.method == "POST":

       session["nome"] = request.form["nome"]
              
       nome = session["nome"]
       em = request.form["email"]
       senha = request.form["senha"]

       us = user(nome=nome, email=em, senha=senha, admin=False,
        	estudante=True)
         

       nser = us.query.filter_by(nome=nome).first()
       eser = us.query.filter_by(email=em).first()

       if nser or eser is not None:
            flash('Nome ou email de usuário existente', 'error')
                  
       else:
           db.session.add(us)
           db.session.commit()

           login_user(us)

           return redirect(url_for("index"))


    return render_template("signup.html")


@app.route("/nova_conta/mentor", methods=["GET", "POST"])
def signup_mentor():
    if request.method == "POST":

       session["nome"] = request.form["nome"]
              
       nome = session["nome"]
       em = request.form["email"]
       senha = request.form["senha"]

       us = user(nome=nome, email=em, senha=senha, admin=True,
        	estudante=False)
         

       nser = us.query.filter_by(nome=nome).first()
       eser = us.query.filter_by(email=em).first()

       if nser or eser is not None:
            flash('Nome ou email de usuário existente', 'error')
                  
       else:
         db.session.add(us)
         db.session.commit()

         login_user(us)

         return redirect(url_for("index"))


    return render_template("signup_mentor.html")

# Google login e signup

# Ajeitar mais tarde

@app.route("/signup-estudante-google", methods=["GET", "POST"])
def signup_estudante_google():
    estado = session['estado']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE_sign_estudante, scopes=SCOPES, state=estado)
    flow.redirect_uri = url_for('google_signup', _external=True)

    auth_resposta = request.url
    flow.fetch_token(authorization_response=auth_resposta)

    
    credenciais = flow.credentials
    session['credenciais'] = credentials_to_dict(credenciais)

    user_info_service = build('oauth2', 'v2', credentials=credenciais)
    user_info = user_info_service.userinfo().get().execute()

    nome = user_info["given_name"]
    email = user_info["email"]
    senha = user_info["id"]

    user = user(nome=nome, email=email, senha=senha, admin=False,
        	estudante=True)
    db.session.add(user)
    db.session.commit()


    session["nome"] = nome

    login_user(user)

    return redirect(url_for('index'))

@app.route("/signup-mentor-google", methods=["GET", "POST"])
def signup_mentor_google():
    estado = session['estado']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE_sign, scopes=SCOPES, state=estado)
    flow.redirect_uri = url_for('google_signup', _external=True)

    auth_resposta = request.url
    flow.fetch_token(authorization_response=auth_resposta)

    
    credenciais = flow.credentials
    session['credenciais'] = credentials_to_dict(credenciais)

    user_info_service = build('oauth2', 'v2', credentials=credenciais)
    user_info = user_info_service.userinfo().get().execute()

    nome = user_info["given_name"]
    email = user_info["email"]
    senha = user_info["id"]

    user = User(nome=nome, email=email, senha=senha, admin=True,
        	estudante=False)
    db.session.add(user)
    db.session.commit()

    session["nome"] = nome

    login_user(user)

    return redirect(url_for('index'))

@app.route("/login-google", methods=["GET", "POST"])
def login_google():
    estado = session['estado']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=estado)
    flow.redirect_uri = url_for('google_login', _external=True)

    auth_resposta = request.url
    flow.fetch_token(authorization_response=auth_resposta)

    
    credenciais = flow.credentials
    session['credenciais'] = credentials_to_dict(credenciais)

    user_info_service = build('oauth2', 'v2', credentials=credenciais)
    user_info = user_info_service.userinfo().get().execute()

    email = user_info['email']
    
    us = user.query.filter_by(email=email).first()

    if us is not None:
        login_user(us)
        nome = us.nome


        session["nome"] = nome

        return redirect(url_for("index"))
    else:
        flash("Usuário inexistente . Se for um erro, faça login na forma convencional .", "error")
        return redirect(url_for("login"))


# Conta

@app.route("/user/<id>")
def ver_conta(id):

    us = user.query.filter_by(id=id).first()

    if us is None:

        return redirect(url_for("error"))

    else:
        nome = us.nome
        
    
    return render_template("ver_perfil.html", nome=nome, us=us)


@app.route("/conta", methods=["GET", "POST"])
@login_required
def conta():
    nome=""
    if "nome" in session:
        nome = session["nome"]

        us = user.query.filter_by(nome=nome).first()

        nome = us.nome
        email = us.email
        senha = us.senha


        if request.method == "POST":

            if request.form.get("remove") == "Excluir":
                item = user.query.filter_by(nome=nome).first()
                db.session.delete(item)
                db.session.commit()

                return redirect("/options")

            elif request.form.get("edit") == "Editar":
                email_novo = request.form["email"]
                senha_nova = request.form["senha"]


                # Alterando os nomes na tabela

                
                us.email = email_novo
                us.senha = senha_nova

                    
                db.session.commit()
                    
    
    return render_template("conta.html", nome=nome, us=us,email=email, senha=senha)

@app.route("/logout")
@login_required
def logout():
    session.pop("nome", None)
    logout_user()

    
    return redirect(url_for("login"))


# Forum

@app.route("/forum")
def forum():
    titles = []
    ids = []


    cur = pergunta.query.all()

    # Transformando uma tupla em strings

    for i in cur:

        ti = "".join(map(str, i.titulo))
                        
        titles.append(ti)

        id_unico = str(i.id)

        id = "".join(map(str, id_unico))
                        
        ids.append(id)

    data = zip(ids, titles)
    
    return render_template("pergunta_list.html", data=data)

@app.route("/questao/<id>")
def questao(id):

    perg = pergunta.query.filter_by(id=id).first()

    if perg is None:

        return redirect(url_for("error"))

    else:
        pergunta_ = perg.titulo
        conteudo = perg.conteudo
    
    return render_template("ver_pergunta.html", conteudo=conteudo,
                           pergunta=pergunta_)

@app.route("/questao/novo", methods=["GET", "POST"])
@login_required
def criar_questao():

    nome = session["nome"]
    
    if request.method == "POST":
              
       titulo = request.form["title"]
       conteudo = request.form["conteudo"]

       perg = pergunta(titulo=titulo, conteudo=conteudo, nome=nome)
        
                  
       
       db.session.add(perg)
       db.session.commit()

       return redirect(url_for("forum"))

    
    return render_template("create_pergunta.html")


# Cursos

@app.route("/cursos")
def cursos():

    titles = []
    ids = []


    cur = curso.query.all()

    # Transformando uma tupla em strings

    for i in cur:

        ti = "".join(map(str, i.titulo_curso))
                        
        titles.append(ti)

        id_unico = str(i.id)

        id = "".join(map(str, id_unico))
                        
        ids.append(id)

    data = zip(ids, titles)
    
    
    return render_template("curso_list.html", data=data)

@app.route("/cursos/<id>")
def ver_curso(id):
    cur = curso.query.filter_by(id=id).first()

    if cur is None:

        return redirect(url_for("error"))

    else:
        curso_nome = cur.titulo_curso
        curso_cont = cur.conteudo_curso
        criador = cur.nome

        
    return render_template("ver_curso.html", nome=curso_nome,
                           sobre = curso_cont)

@app.route("/cursos/novo", methods=["GET", "POST"])
@login_required
def criar_curso():
    nome = session["nome"]
    
    if request.method == "POST":
              
       titulo = request.form["title"]
       conteudo = request.form["conteudo"]

       curs = curso(titulo_curso=titulo, conteudo_curso=conteudo, nome=nome)
        
                  
       
       db.session.add(curs)
       db.session.commit()

       return redirect(url_for("cursos"))
    
    return render_template("create_curso.html")


# Comunidade

@app.route("/grupos")
def grupos():
    titles = []
    ids = []


    gru = grupo.query.all()

    # Transformando uma tupla em strings

    for i in gru:

        ti = "".join(map(str, i.titulo))
                        
        titles.append(ti)

        id_unico = str(i.id)

        id = "".join(map(str, id_unico))
                        
        ids.append(id)

    data = zip(ids, titles)
    
    return render_template("chat_list.html", data=data)

@app.route("/grupos/<id>")
def ver_grupos(id):
    gru = grupo.query.filter_by(id=id).first()

    if gru is None:

        return redirect(url_for("error"))

    else:
        gru_nome = gru.titulo
        gru_cont = gru.conteudo
    
    return render_template("comunidade.html", grupo=gru_nome,
                           gru_desc = gru_cont)

@app.route("/grupos/novo", methods=["GET", "POST"])
@login_required
def create_grupos():
    nome = session["nome"]
    
    if request.method == "POST":
              
       titulo = request.form["title"]
       conteudo = request.form["conteudo"]

       gru = grupo(titulo=titulo, conteudo=conteudo, nome=nome)
        
                  
       
       db.session.add(gru)
       db.session.commit()

       return redirect(url_for("grupos"))
    return render_template("create_grupo.html")


# Esse trecho roda o site, podemos usar na forma simplificada:
# app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True, port=5010)
