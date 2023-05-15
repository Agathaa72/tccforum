
# O código principal

from flask import flask



# Aqui é uma das rotas, aqui ficará a landing page


@app.route("/")
def inicio():
	return render_template("site.html") # Criar mais tarde


# Esse trecho roda o site, podemos usar na forma simplificada:
# app.run(debug=True)

if __name__ == "__main__":
	app.run(debug=True)