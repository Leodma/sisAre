from app import db
from datetime import datetime
from app.cadastros.models import Unidades

class Termo(db.Model):
    __tablename__ = 'termocompromisso'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    processo_numero = db.Column(db.String(60), nullable=False)
    anexo = db.Column(db.String(11), nullable=False)
    finalidade = db.Column(db.Text)
    tc_firmado = db.Column(db.String(45))
    numero_tc_firmado = db.Column(db.String(30))
    unidade = db.Column(db.Integer)

    def __init__(self, processo_numero, anexo, finalidade, tc_firmado, numero_tc_firmado, unidade):
        self.processo_numero = processo_numero
        self.anexo = anexo
        self.finalidade = finalidade
        self.tc_firmado = tc_firmado
        self.numero_tc_firmado = numero_tc_firmado
        self.unidade = unidade
    
    def __repr__(self):
        return self.titulo

 
