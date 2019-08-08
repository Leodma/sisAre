from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, ValidationError

class BuscaForm(FlaskForm):
    busca = StringField('Digite o conteúdo da busca', validators=[DataRequired(message=('Insira um texto para a busca'))])
    criterio_cad = SelectField('Campos de Busca para Cadastro', choices=[], validators=[DataRequired(message='Selecione uma opção')])
    criterio_termo = SelectField('Campos de Busca para Termo de Compromisso', choices=[], validators=[DataRequired(message='Selecione uma opção')])
    submit = SubmitField('Buscar')