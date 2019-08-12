#app/tc/routes.py

from app.tc import termos
from app import db
from app.tc.models import Termo
from app.auth.models import User
from app.cadastros.models import Unidades, AtualizacaoCadastro
from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required, login_user, current_user
from app.tc.forms import TermoForm

#lista de anexos para os formularios
lista_anexos = [(None,'Selecione uma opção') ,('Anexo I', 'Anexo I'),('Anexo II', 'Anexo II'),('Anexo III', 'Anexo III'),('Anexo IV', 'Anexo IV'),('Anexo V', 'Anexo V'),('Anexo VI', 'Anexo VI'), ('Anexo VII', 'Anexo VII')]

@termos.route('/inserirtermo', methods=['GET', 'POST'])
@login_required
def insere_termo():

    if current_user.user_cat =='Conv':
        return redirect(url_for('authentication.acesso_negado'))
    
    form = TermoForm()
    form.anexo.choices= lista_anexos
    form.unidade.choices =[(unidade.id,unidade.nome) for unidade in Unidades.query.order_by(Unidades.nome).all()]
    usuario = current_user

    if form.validate_on_submit():
        termo = Termo(
            processo_numero = form.processo_numero.data,
            anexo = form.anexo.data,
            finalidade = form.finalidade.data,
            tc_firmado = form.tc_firmado.data,
            numero_tc_firmado = form.numero_tc_firmado.data, 
            unidade = form.unidade.data 
        )
        db.session.add(termo)
        
        atualizacao = AtualizacaoCadastro( numero_cadastro = ' ', numero_termo=form.processo_numero.data, tipo = 'Inclusão', id_usuario=usuario.id)
        db.session.add(atualizacao)         
        db.session.commit()

        flash('Termo de compromisso adicionado com sucesso')
        return redirect(url_for('main.index'))
    
    return render_template('insere_termo.html', form = form)

@termos.route('/lista_termos_unidades')
@login_required
def termo_por_unidade():
    termo =  Termo.query.all()
    unidades = Unidades.query.order_by(Unidades.nome).all()
    
    return render_template('lista_termos_geral_unidade.html', termos=termo, unidades = unidades)

@termos.route('/termos_unidade/<id_ud>')
@login_required
def termos_da_unidade(id_ud):
    termos = Termo.query.filter_by(unidade = id_ud).all()
    unidade = Unidades.query.get(id_ud)

    return render_template('lista_termo_unidade.html', termos = termos, unidade = unidade)

@termos.route('/termo/<termo_id>')
@login_required
def termo_compromisso(termo_id):
    termo = Termo.query.get(termo_id)
    unidade = Unidades.query.get(termo.unidade)
    return render_template('termo_compromisso.html', termo = termo, unidade=unidade)

@termos.route('/termo_home/<numero_termo>')
@login_required
def termo_numero(numero_termo):
    termo = Termo.query.filter_by(processo_numero = numero_termo).first()
    unidade = Unidades.query.get(termo.unidade)
    return render_template('termo_compromisso.html', termo = termo, unidade=unidade)

@termos.route('/editar_termo/<termo_id>', methods=['GET', 'POST'])
@login_required
def editar_termo(termo_id):
    
    if current_user.user_cat =='Conv':
        return redirect(url_for('authentication.acesso_negado'))
    
    termo = Termo.query.get(termo_id)
    form = TermoForm(obj=termo)
    form.unidade.choices =[(unidade.id,unidade.nome) for unidade in Unidades.query.order_by(Unidades.nome).all()]
    form.anexo.choices = lista_anexos
    usuario = current_user
    if form.validate_on_submit():
        termo.processo_numero = form.processo_numero.data
        termo.anexo = form.anexo.data
        termo.finalidade = form.finalidade.data
        termo.tc_firmado = form.numero_tc_firmado.data
        termo.numero_tc_firmado = form.numero_tc_firmado.data

        db.session.add(termo)

        atualizacao = AtualizacaoCadastro(numero_cadastro = ' ',numero_termo=form.processo_numero.data, tipo = 'Alteração',id_usuario=usuario.id)
        db.session.add(atualizacao)         
        db.session.commit()

        flash('Termo de compromisso atualizado')
        return redirect(url_for('termos.termo_por_unidade'))
    return render_template('editar_termo.html', form=form)
 
@termos.route('/deletar/termo/<termo_id>',methods=['GET', 'POST'])
@login_required
def deletar_termo(termo_id):

    if current_user.user_cat =='Conv':
        flash('Voce não tem permissão para deletar termos de compromisso')
        return redirect(url_for('authentication.acesso_negado'))
    
    termo = Termo.query.get(termo_id)
    
    
    if request.method == 'POST':
        usuario = current_user
        atualizacao = AtualizacaoCadastro(  numero_cadastro = ' ', numero_termo = termo.processo_numero, tipo = 'Exclusão',  id_usuario=usuario.id)
        
        db.session.delete(termo)
        db.session.add(atualizacao)         
        db.session.commit()

        flash('Termo de Compromisso apagado com sucesso')
        return redirect(url_for('main.index'))
    return render_template('deleta_termo.html', termo = termo)