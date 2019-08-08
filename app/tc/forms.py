from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField,IntegerField, FloatField, SelectField, SelectMultipleField, RadioField, TextAreaField, Form, FieldList, FormField
from wtforms.fields.html5 import DateField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import DataRequired, Length, ValidationError


class TermoForm(FlaskForm):
    processo_numero = StringField('Numero do Processo', validators=[DataRequired(message=("Inserir Numero"))])
    anexo = SelectField('Anexo', choices=[], validators=[DataRequired(message='É obrigatório inserir o anexo')])
    finalidade = TextAreaField('Finalidade')
    tc_firmado = SelectField('Termo de Compromisso Firmado', choices=[('Sim', 'Sim'), ('Não', 'Não'), ('analise', 'Em Análise')])
    numero_tc_firmado = StringField('Numero do Termo de Compromisso Firmado')
    unidade = SelectField('Unidade', choices=[], coerce=int)
    submit = SubmitField('Inserir/Atualizar')
    

