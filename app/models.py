# Aqui fica o banco de dados

from flask_login import UserMixin
from app import db, login

# Tabelas

@login.user_loader
def get_user(user_id):
    user= User.query.filter_by(id=user_id).first()
    if user:
        return user
    return None

class user(db.Model, UserMixin):
    __tablename__  = "user"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(80))
    senha = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    estudante = db.Column(db.Boolean)

    def __init__(self, nome, email, senha, admin, estudante):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.admin = admin
        self.estudante = estudante
