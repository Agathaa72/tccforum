
'''

	Criado por: dcgo15 


'''


# O código principal

from flask import flask, render_template
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

@app.route("/options")
def opcao_conta():
	return render_template("opcao.html")


@app.route("/login")
def login():
	return render_template("login.html")


@app.route("/nova_conta/estudante")
def signup_estudante():
	return render_template("signup.html")


@app.route("/nova_conta/mentor")
def signup_mentor():
	return render_template("signup.html")

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
	app.run(debug=True)