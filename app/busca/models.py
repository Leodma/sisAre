from app import db
from datetime import datetime
from app.cadastros.models import Unidades

class Termo(db.Model):
    __tablename__ = 'termocompromisso'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(250), nullable=False)
    anexo = db.Column(db.String(11), nullable=False)
    conteudo = db.Column(db.Text)
    unidade = db.Column(db.Integer)

    def __init__(self, titulo, anexo, conteudo, unidade):
        self.titulo = titulo
        self.anexo = anexo
        self.conteudo = conteudo
        self.unidade = unidade
    
    def __repr__(self):
        return self.titulo
