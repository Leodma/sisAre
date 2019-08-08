from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.auth.models import User
from flask_login import current_user


def email_check(form, field): # definição de um validador do wtf personalizado.
    email = User.query.filter_by(user_email=field.data).first()
    if email:
        raise ValidationError('Esse email já existe')

def emai_update_check(form, field):
    user = User.query.filter_by(user_email=field.data).first()
    if user.user_name !=form.user_name:
        raise ValidationError('Esse email já existe')

def password_check(form, field): # validador para alteração de senha.
    
    if not current_user.check_password(field.data):
        raise ValidationError('A senha antiga não confere')



class RegistrationForm(FlaskForm):
    nome = StringField('Nome:',validators=[DataRequired(),Length(3,15,message='entre 3 e 15 caracteres')])
    email = StringField('Email:', validators=[DataRequired(),Email('email inválido'),email_check])
    nivel = SelectField('Categoria:', choices=[(None,'Selecione o Nível de Acesso'),('Conv', 'Convidado'), ('Edit', 'Editor'),('Adm', 'Administrador') ], validators=[DataRequired()])
    password = PasswordField('Senha ', validators=[DataRequired(), Length(5, message="A senha deve conter no mínimo 5 caracteres"), EqualTo('confirm', message='A senha não confere')])
    confirm = PasswordField('Confirmação de Senha ', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email('email invalido')])
    password = PasswordField('Senha', validators=[DataRequired()])
    stay_loggedin = BooleanField('Permanecer conectado')
    submit = SubmitField('Entrar')


class UserForm(FlaskForm):
    user_name = StringField('Nome:',validators=[DataRequired(),Length(3,15,message='entre 3 e 15 caracteres')])
    user_email = StringField('Email:', validators=[DataRequired(),Email('email inválido'), emai_update_check])
    user_cat = SelectField('Categoria:', choices=[(None,'Selecione o Nível de Acesso'),('Conv', 'Convidado'), ('Edit', 'Editor'),('Adm', 'Administrador') ], validators=[DataRequired()])
    submit = SubmitField('Atualizar')


class AlterarSenha(FlaskForm):
    old_password = PasswordField('Senha Antiga ', validators=[DataRequired(), password_check])
    password = PasswordField('Nova Senha ', validators=[DataRequired(), Length(5, message="A senha deve conter no mínimo 5 caracteres"), EqualTo('confirm', message='A nova senha não confere')])
    confirm = PasswordField('Confirmação de Senha ', validators=[DataRequired()])
    submit = SubmitField('Alterar Senha')
    
