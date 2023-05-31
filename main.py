
'''

	Criado por: dcgo15 


'''


# O código principal

from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user, login_required
from app.models import *
from app import app, models


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

       eser = user.query.filter_by(email=em).first()
       
       sser = user.query.filter_by(senha=senha).first()

       if eser is None and sser is None:
            flash('Usuário inexistente ou dados incorretos', 'error')
                  
       else:

           session["nome"] = eser.nome

           login_user(user)

           return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/nova_conta/estudante", methods=["GET", "POST"])
def signup_estudante():
    if request.method == "POST":

       session["nome"] = request.form["nome"]
              
       nome = session["nome"]
       em = request.form["email"]
       senha = request.form["senha"]

       user = user(nome=nome, email=em, senha=senha, admin=False,
        	estudante=True)
         

       nser = user.query.filter_by(nome=nome).first()
       eser = user.query.filter_by(email=em).first()

       if nser or eser is not None:
            flash('Nome ou email de usuário existente', 'error')
                  
       else:
           db.session.add(user)
           db.session.commit()

           login_user(user)

           return redirect(url_for("index"))


    return render_template("signup.html")


@app.route("/nova_conta/mentor", methods=["GET", "POST"])
def signup_mentor():
    if request.method == "POST":

       session["nome"] = request.form["nome"]
              
       nome = session["nome"]
       em = request.form["email"]
       senha = request.form["senha"]

       user = user(nome=nome, email=em, senha=senha, admin=True,
        	estudante=False)
         

       nser = user.query.filter_by(nome=nome).first()
       eser = user.query.filter_by(email=em).first()

       if nser or eser is not None:
            flash('Nome ou email de usuário existente', 'error')
                  
       else:
         db.session.add(user)
         db.session.commit()

         login_user(user)

         return redirect(url_for("index"))


    return render_template("signup_mentor.html")

# Conta

@app.route("/user/<id>")
def ver_conta(id):
    return render_template("ver_perfil.html")


@app.route("/conta")
def conta():
    return render_template("conta.html")

@app.route("/logout")
def logout():
    pass


# Forum

@app.route("/forum")
def forum():
    return render_template("forum.html")

@app.route("/questao/<id>")
def questao(id):
    return render_template("ver_pergunta.html")

@app.route("/questao/novo")
def criar_questao():
    return render_template("create_pergunta.html")


# Cursos

@app.route("/cursos")
def curso():
    return render_template("curso.html")

@app.route("/cursos/<id>")
def ver_curso(id):
    return render_template("ver_curso.html")

@app.route("/cursos/novo")
def criar_curso():
    return render_template("create_curso.html")


# Comunidade

@app.route("/grupos")
def grupos():
    return render_template("chat.html")

@app.route("/grupos/<id>")
def ver_grupos(id):
    return render_template("ver_grupo.html")

@app.route("/grupos/novo")
def create_grupos():
    return render_template("create_grupo.html")


# Esse trecho roda o site, podemos usar na forma simplificada:
# app.run(debug=True)

if __name__ == "__main__":
	app.run(debug=True, port=5003)
