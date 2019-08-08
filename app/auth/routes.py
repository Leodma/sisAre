from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.auth.forms import RegistrationForm, LoginForm, UserForm, AlterarSenha
from app.auth import authentication as at
from app.cadastros import main
from app.auth.models import User
from app import db

@at.route('/registrar', methods=['GET','POST'])
@login_required
def register_user():

    if current_user.user_cat != 'Adm':
        return redirect(url_for('authentication.acesso_negado'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        User.create_user(
            user=form.nome.data,
            email=form.email.data,
            nivel = form.nivel.data,
            password=form.password.data)
        flash(f' Usuário {form.nome.data} registrado com sucesso')
        return redirect(url_for('authentication.do_the_login'))
   
    return render_template('insere_usuario.html',form=form)


@at.route('/login', methods=['GET','POST'])
def do_the_login():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
   
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Nome de usuário ou senha incorretos', 'error')
            return redirect(url_for('authentication.do_the_login'))
    
        login_user(user, form.stay_loggedin.data)
        return redirect(url_for('main.index'))

    return render_template('login.html', form=form)

@at.route('/logout')
@login_required
def log_out_user():
    logout_user()
    return redirect(url_for('authentication.do_the_login'))

@at.route('/acessonegado')
def acesso_negado():
    return render_template('acesso_negado.html')


@at.route('/meusdados')
@login_required
def meus_dados( ):
    return render_template("meus_dados.html",user=current_user)

@at.route('/gerenciar_usuario')
@login_required
def gerenciar_usuario():
    usuarios = User.query.order_by(User.user_name).all()
    return render_template('gerencia_usuarios.html', usuarios = usuarios)

@at.route('/editar_usuario/<user_id>', methods=['GET','POST'])
@login_required
def editar_usuario(user_id):
    usuario = User.query.get(user_id)
    if usuario.user_cat == 'Adm' and  current_user.user_email != usuario.user_email :
        return redirect(url_for('authentication.acesso_negado'))
    
    form = UserForm(obj=usuario)

    if form.validate_on_submit():
        usuario.user_name = form.user_name.data
        usuario.user_email = form.user_email.data
        usuario.user_cat = form.user_cat.data
        
        db.session.add(usuario)
        db.session.commit()

        flash(f'Dados do Usuário {usuario.user_name} alterados com sucesso')
        return redirect(url_for('main.lista_responsaveis'))

    return render_template('edita_dados.html' ,form = form)

@at.route('/excluir_usuario/<user_id>')
@login_required
def deletar_usuario(user_id):
    usuario = User.query.get(user_id)
    
    if current_user.user_cat != 'Adm' or  current_user.user_email == usuario.user_email:
        flash(f'Você não tem permissão para excluir o usuário {usuario.user_name}')
        return redirect(url_for('authentication.gerenciar_usuario'))
    
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario apagado com sucesso')
    return redirect(url_for('authentication.gerenciar_usuario'))


@at.route('/alterar_senha', methods=['GET','POST'])
@login_required
def alterar_senha( ):
    usuario = User.query.get(current_user.id)
    form = AlterarSenha()
    if form.validate_on_submit():
        usuario.altera_senha(form.password.data)
        db.session.add(usuario)
        db.session.commit()
        flash('Senha Alterada com Sucesso - Favor entrar novamente')
        return redirect(url_for('authentication.log_out_user'))
    return render_template('altera_senha.html', form=form)

@at.app_errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404

     
    
    


    
