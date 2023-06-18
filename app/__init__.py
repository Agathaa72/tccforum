# O __init__ é o incializador do programa: main.py

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from flask_socketio import SocketIO, emit, send, join_room, leave_room

'''
	
	servidor online: "mysql+pymysql://keysapp:META100K@db4free.net/knowzone"
	servidor local: "mysql+pymysql://root:META100Kk#@localhost/knowzone"

'''


app = Flask(__name__)

# Banco de dados

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:META100Kk#@localhost/knowzone"
app.config["SECRET_KEY"] = "wZc3w7Am3hPMaFp3jqrhxASdRBHcydpEHiKaAp7xgtp"

# Variaveis de login manager, db e oauth

login = LoginManager(app)
db = SQLAlchemy(app)
io = SocketIO(app)
oauth = OAuth(app)

# login e signup

login.login_view = "login_google"
login.login_view = "signup_estudante_google"
login.login_view = "signup_mentor_google"
login.login_view = "signup_estudante"
login.login_view = "signup_mentor"
login.login_view = "login"
