# O __init__ é o incializador do programa: main.py

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth

'''
	
	servidor online: "mysql+pymysql://keysapp:META100K@db4free.net/knowzone"
	servidor local: "mysql+pymysql://root:META100Kk#@localhost/knowzone"

'''


app = Flask(__name__)

# Banco de dados

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://keysapp:META100K@db4free.net/knowzone"
app.config["SECRET_KEY"] = "wZc3w7Am3hPMaFp3jqrhxASdRBHcydpEHiKaAp7xgtp"

# Variaveis de login manager, db e oauth

login = LoginManager(app)

db = SQLAlchemy(app)
oauth = OAuth(app)

# login e signup

login.login_view = "login"
login.login_view = "signup"
