from app import db
from datetime import datetime
from app.auth.models import User

# criar  um modelo para os termos de compromisso - Relacionamento 1 - N (ud - termos)
# criar  um modelo para controle de acesso aos cadastros ( Usuario(FK) - N. Cadastro(FK) - data ( alteração ou inclusão))

class Responsavel(db.Model):
    __tablename__ = 'responsavel'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, index=True)
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(30))
    instituicao = db.Column(db.String(200))
    
    def __init__(self, nome, cpf, telefone, email, instituicao):
      
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.instituicao = instituicao


    def __repr__(self):
        return f' {self.nome} -- {self.cpf}'


     # classmethod não é associado a instância, é utilizado pela classe em si.
    @classmethod
    def cria_responsavel(cls, nome, cpf): # - CLS é a classe passada como parametro.
        responsavel = cls( nome=nome,cpf =cpf)
        db.session.add(responsavel)
        db.session.commit()
        return responsavel

class Unidades(db.Model):
    __tablename__ = 'unidades'
    __table_args__ = __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(14), nullable=False, unique=True)
    nome  = db.Column(db.String(150))
    endereco = db.Column(db.String(100))
    cidade  = db.Column(db.String(50))
    estado = db.Column(db.String(2))
    cep = db.Column(db.String(8)) 
    chefe_geral = db.Column(db.String(60))
    telefone = db.Column(db.String(15))
 

    def __init__(self, id, cnpj,nome,endereco,cidade,estado,chefe_geral,telefone ):
        self.id = id
        self.cnpj = cnpj
        self.nome = nome
        self.endereco = endereco
        self.cidade = cidade
        self.estado = estado
        self.chefe_geral = chefe_geral
        self.telefone = telefone
    

    def __repr__(self):
        return self.nome

class Cadastro(db.Model):
    __tablename__ = 'cadastros'
    __table_args__ = {'extend_existing': True} 

    numero = db.Column(db.String(8), primary_key=True)
    unidade = db.Column(db.Text, nullable=False, index=True)
    acesso = db.Column(db.String(100), nullable=False)
    titulo = db.Column(db.Text, nullable=False)
    data_cadastro = db.Column(db.String, nullable=False)
    situacao = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(300), nullable=False)
    modalidade = db.Column(db.String(100), nullable=False)
    finalidade = db.Column(db.String(100), nullable=False)
    aut_inst = db.Column(db.String(100))
    aut_processo = db.Column(db.String(100))
    aut_numero = db.Column(db.String(100))
    aut_validade = db.Column(db.String(30))
    curb = db.Column(db.String(100))
    data_inicio = db.Column(db.String(300), nullable=False)
    data_fim = db.Column(db.String(300), nullable=False)
    membro_nome = db.Column(db.Text, nullable=False)
    membro_instituicao = db.Column(db.Text, nullable=False)
    componente_tipo = db.Column(db.Text, nullable=False)
    componente_especie = db.Column(db.Text, nullable=False)
    raca_local = db.Column(db.String(50))
    envio_amostra = db.Column(db.String(300))
    cta = db.Column(db.String(300))
    componente_acessado = db.Column(db.String(300))
    atualizacao = db.relationship('AtualizacaoCadastro', backref='owner', lazy='dynamic')

    def __init__(self,numero, unidade, acesso, titulo, data_cadastro, situacao, cpf, modalidade, finalidade, aut_inst, aut_processo, aut_numero , aut_validade, curb, data_inicio,data_fim, membro_nome, membro_instituicao, componente_tipo, componente_especie, raca_local, envio_amostra, cta, componente_acessado):
        self.numero = numero
        self.unidade = unidade
        self.acesso = acesso
        self.titulo = titulo
        self.data_cadastro = data_cadastro
        self.situacao = situacao
        self.cpf = cpf
        self.modalidade = modalidade
        self.finalidade = finalidade
        self.aut_inst = aut_inst
        self.aut_processo = aut_processo
        self.aut_numero = aut_numero
        self.aut_validade = aut_validade
        self.curb = curb
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.membro_nome = membro_nome
        self.membro_instituicao = membro_instituicao
        self.componente_tipo = componente_tipo
        self.componente_especie = componente_especie
        self.raca_local = raca_local
        self.envio_amostra = envio_amostra
        self.cta = cta
        self.componente_acessado = componente_acessado        

    def __repr__(self):
        return f'{self.numero} by {self.titulo}'

    @classmethod
    def getat(cls, criterio):
        for att in cls.attribute:
            if att == criterio:
                return att

            

class AtualizacaoCadastro(db.Model):
    __tablename__ = 'atualizacao'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    numero_cadastro = db.Column(db.String(20), db.ForeignKey('cadastros.numero'))
    numero_termo = db.Column(db.String(45))
    tipo = db.Column(db.String(45)) #alteração  inclusão exclusão
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    data_atualizacao = db.Column(db.DateTime, default=datetime.now) 

    def __init__(self, numero_cadastro, numero_termo, tipo, id_usuario):
        self.numero_cadastro = numero_cadastro
        self.numero_termo=numero_termo
        self.tipo=tipo
        self.id_usuario=id_usuario

    @classmethod
    def atualiza_dados_cadastro(cls, numero_cadastro, tipo ,id_usuario) : # - CLS é a classe passada como parametro.
        dados = cls( numero_cadastro=numero_cadastro.upper(), numero_termo = '',tipo = tipo, id_usuario = id_usuario)
        db.session.add(dados)
        db.session.commit()
        return dados

 
        
    

  
    
  

