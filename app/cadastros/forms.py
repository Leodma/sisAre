from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField,IntegerField, FloatField, SelectField, SelectMultipleField, RadioField, TextAreaField, Form, FieldList, FormField
from wtforms.fields.html5 import DateField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import DataRequired, Length, ValidationError
from app.cadastros.models import Cadastro, Unidades



def verfica_cadastro(form, field): # validador de cadastro existente
    cadastro = Cadastro.query.get(field.data.upper())
    if cadastro:
        raise ValidationError('Esse número já está cadastrado ou está incorreto.')



class MultiCheckbox(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

# class CPFSubform(Form):
#     # Subformulario para adicionar campos dinamicamente ao formulario para responsaveis do cadastro
#     responsavel = StringField('Responsável:')
#     cpf = StringField('CPF')

class CriaCadastro(FlaskForm):
    numero = StringField('Numero do Cadastro', validators=[DataRequired(message='O número do cadastro é obrigatório'), Length(min=7,max=8 ,message='O número do cadastro deve possuir entre 7 e 8 caracteres'),verfica_cadastro])
    unidade = SelectField('Unidade', choices=[], validators=[DataRequired(message='É obrigatório inserir o nome da unidade')])
    titulo = StringField('Titulo do Projeto', validators=[DataRequired(message=('Preencimento Obrigatório'))])
    acesso =SelectField('Objeto do Acesso',choices=[(None,'Selecione uma opção'),('Patrimônio Genético', 'Patrimônio Genético'), ('Conhecimento Tradicional Associado', 'Conhecimento Tradicional Associado'), ('Patrimônio Genético e Conhecimento Tradicional Associado','Patrimônio Genético e Conhecimento Tradicional Associado')], validators=[DataRequired(message='Campo Obrigatório')])
    data_cadastro = DateField('Data do Cadastro',  format='%Y-%m-%d',validators=[DataRequired(message=('Preenchimento Obrigatório'))])
    situacao = SelectField('Situação', choices=[(None,'Selecione uma opção'),('Aguardando Revisão', 'Aguardando Revisão'),('Concluído','Concluído'),('Revisado','Revisado')], validators=[DataRequired(message='Selecione uma das opções')])
    responsavel = TextAreaField('Responsável')
    cpf = TextAreaField('CPF do Responsável')
    modalidade = SelectField('Modalidade', choices=[(None,'Selecione uma opção'),('Regularização', 'Regularização'), ('Cadastro Novo', 'Cadastro Novo'),('Adequação','Adequaçao')], validators=[DataRequired(message='Selecione uma das opções')])
    finalidade = MultiCheckbox('Finalidade do Acesso',choices=[('Pesquisa','Pesquisa'),('Bioprospecção', 'Bioprospecção'),('Desenvolvimento Tecnológico','Desenvolvimento Tecnológico'),('Pesquisa e Desenvolvimento Tecnológico','Pesquisa e Desenvolvimento Tecnológico')], validators=[DataRequired(message=('Selecione uma das opções'))])
    aut_inst = StringField('Autorizacao Instituicao')
    aut_processo = StringField('Numero do Processo')
    aut_numero = StringField('Numero da Autorização')
    aut_validade = StringField('Data da Validade da Autorização')
    curb = RadioField('CURB', choices=[('sim','Sim'),('nao','Não')])
    data_inicio = StringField('Data Inicio:')
    data_fim = StringField('Data Fim')
    membro_nome = TextAreaField("Membros Instituição")
    membro_instituicao = TextAreaField('Instituição')
    componente_tipo = TextAreaField('Tipo do Componente')
    componente_especie = TextAreaField('Especie Componente')
    raca_local = StringField('Raça Localmente Adaptada')
    envio_amostra = RadioField('Envio de Amostra:',choices=[('sim','Sim'),('nao','Não')], validators=[DataRequired(message='Selecione uma das opções')])
    cta = SelectField('Conhecimento Tradicional Associado:',choices=[(None,'Selecione uma opção'),('Sim Origem Identificável', 'Sim Origem Identificável'), ('Sim Origem Não Identificável', 'Sim Origem Não Identificável'), ('Não', 'Não')])
    componente_acessado = StringField('Conhecimento Tradicional Associado Acessado')
    submit = SubmitField('Inserir')


class EditaCadastroForm(FlaskForm):
    numero = StringField('Numero do Cadastro', validators=[DataRequired(message='O número do cadastro é obrigatório'), Length(min=8,max=8, message='O número do cadastro deve ter 8 caracteres')])
    unidade = SelectField('Unidade', choices=[], validators=[DataRequired(message='É obrigatório inserir o nome da unidade')])
    titulo = StringField('Titulo do Projeto', validators=[DataRequired(message=('Preencimento Obrigatório'))])
    acesso =SelectField('Objeto do Acesso',choices=[(None,'Selecione uma opção'),('Patrimônio Genético', 'Patrimônio Genético'), ('Conhecimento Tradicional Associado', 'Conhecimento Tradicional Associado'), ('Patrimônio Genético e Conhecimento Tradicional Associado','Patrimônio Genético e Conhecimento Tradicional Associado')], validators=[DataRequired(message='Campo Obrigatório')])
    data_cadastro = DateField('Data do Cadastro',  format='%Y-%m-%d',validators=[DataRequired(message=('Preenchimento Obrigatório'))])
    situacao = SelectField('Situação', choices=[(None,'Selecione uma opção'),('Aguardando Revisão', 'Aguardando Revisão'),('Concluído','Concluído'),('Revisado','Revisado')], validators=[DataRequired(message='Selecione uma das opções')])
    responsavel = TextAreaField('Responsável')
    cpf = TextAreaField('CPF do Responsável')
    modalidade = SelectField('Modalidade', choices=[(None,'Selecione uma opção'),('Regularização', 'Regularização'), ('Cadastro Novo', 'Cadastro Novo'),('Adequação','Adequaçao')], validators=[DataRequired(message='Selecione uma das opções')])
    finalidade = MultiCheckbox('Finalidade do Acesso',choices=[('Pesquisa','Pesquisa'),('Bioprospecção', 'Bioprospecção'),('Desenvolvimento Tecnológico','Desenvolvimento Tecnológico'),('Pesquisa e Desenvolvimento Tecnológico','Pesquisa e Desenvolvimento Tecnológico')], validators=[DataRequired(message=('Selecione uma das opções'))])
    aut_inst = StringField('Autorizacao Instituicao')
    aut_processo = StringField('Numero do Processo')
    aut_numero = StringField('Numero da Autorização')
    aut_validade = StringField('Data da Validade da Autorização', default=None)
    curb = RadioField('CURB', choices=[('sim','Sim'),('nao','Não')])
    data_inicio = StringField('Data Inicio:')
    data_fim = StringField('Data Fim')
    membro_nome = TextAreaField("Membros Instituição")
    membro_instituicao = TextAreaField('Instituição')
    componente_tipo = TextAreaField('Tipo do Componente')
    componente_especie = TextAreaField('Especie Componente')
    raca_local = StringField('Raça Localmente Adaptada')
    envio_amostra = RadioField('Envio de Amostra:',choices=[('sim','Sim'),('nao','Não')], validators=[DataRequired(message='Selecione uma das opções')])
    cta = SelectField('Conhecimento Tradicional Associado:',choices=[('Sim Origem Identificável', 'Sim Origem Identificável'), ('Sim Origem Não Identificável', 'Sim Origem Não Identificável'), ('Não', 'Não')])
    componente_acessado = StringField('Conhecimento Tradicional Associado Acessado')
    submit = SubmitField('Inserir')
    
class ResponsavelForm(FlaskForm):
    nome = StringField('Nome')
    cpf = StringField('CPF')
    telefone = StringField('Telefone')
    email = StringField('Email')
    instituicao = SelectField('Unidade', choices=[])
    submit = SubmitField('Enviar')

class UnidadeForm(FlaskForm):
    cnpj = StringField('CNPJ')
    endereco = StringField('Endereço')
    cidade = StringField('Cidade')
    estado = SelectField('Estado', choices=[])
    cep = StringField('Cep')
    chefe_geral = StringField('Chefe-Geral')
    telefone = StringField('Telefone')
    submit = SubmitField('Enviar')

