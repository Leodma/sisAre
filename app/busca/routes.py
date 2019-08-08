from app import db
from app.busca import buscar
from app.cadastros.models import Cadastro
from app.tc.models import Termo
from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required, login_user, current_user, login_required
from app.busca.forms import BuscaForm


@buscar.route('/busca' , methods=['GET', 'POST'])
@login_required
def busca():
    
    opcoes_cadastro = [('numero', 'Número'), ('titulo','Título'),('cpf', 'CPF'), ('modalidade', 'Modalidade')]
    opcoes_termo = [('titulo','titulo'),('anexo', 'anexo'), ('conteudo','conteudo')]
    form = BuscaForm()

    form.criterio_cad.choices = opcoes_cadastro
    form.criterio_termo.choices = opcoes_termo
    if request.args.get('bd'):
        tipo =  request.args.get('bd')
    else:
        tipo = 'Cadastros'

    if request.method == 'POST':
        busca = form.busca.data

        if tipo == "Cadastros":
            criterio = form.criterio_cad.data 
        else:
            criterio = form.criterio_termo.data
        
       
        return redirect(url_for('buscar.busca_conteudo', tipo = tipo, criterio = criterio, conteudo = busca))
    
    return render_template('busca.html', form=form)


@buscar.route('/busca/<tipo>/<criterio>/<conteudo>')
@login_required
def busca_conteudo(tipo, criterio, conteudo):
    tipo = tipo
    criterio = criterio
    conteudo = conteudo
    
    if tipo == 'Cadastros':
        cadastros = Cadastro.query.filter(Cadastro.__dict__.__getitem__(criterio).like(f'%{conteudo}%')).all()
        return render_template('lista_cadastros.html', cadastros=cadastros, titulo = f'Cadastros encontrados com: {conteudo}' )

    if tipo =='Termo de Compromisso':
        termos = Termo.query.filter(Termo.__dict__.__getitem__(criterio).like(f'%{conteudo}%')).all()
        return render_template('lista_termos.html', termos=termos, titulo = f'Termos encontrados com: {conteudo}' ) 
