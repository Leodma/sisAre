#capp/cadastros/routes.py

import os
from app.cadastros import main
from app import db
from app.cadastros.helpers import tira_paragrafo, cria_lista, lista_para_texto, cria_lista_db, cria_texto_formulario, troca_por_nulo, porcentagem
from app.cadastros.models import Responsavel, Cadastro, Unidades, AtualizacaoCadastro
from app.auth.models import User
from flask import render_template, flash, request, redirect, url_for, send_from_directory
from flask_login import login_required, login_user, current_user, login_required
from app.cadastros.forms import CriaCadastro, ResponsavelForm, UnidadeForm, EditaCadastroForm



@main.route('/')
@login_required
def index():
    #quantitativos para o gráfico.
    total_cadastros = Cadastro.query.count()
    regulariza = Cadastro.query.filter_by(modalidade='Regularização').count()
    novo = Cadastro.query.filter_by(modalidade='Cadastro Novo').count()
    adequa = Cadastro.query.filter_by(modalidade='Adequação').count()
    graph = [1,1,1,0,0,0]
    if regulariza and novo and adequa:
        graph = [   porcentagem(regulariza, total_cadastros),
                    porcentagem(novo, total_cadastros),
                    porcentagem(adequa, total_cadastros),
                    regulariza, novo, adequa
                ]
    user= User.query.all()
    atualizacoes = AtualizacaoCadastro.query.order_by(db.desc('data_atualizacao')).limit(20)
   
    return render_template('home.html', atualizacoes = atualizacoes, user=user, total = total_cadastros, graph =graph)

    # Relatorio Por Unidade

@main.route('/cadastros')
@login_required
def lista_cadastros(): 
    cadastros = Cadastro.query.limit(50)
    #numero = Cadastros.query.count()
    return render_template('lista_cadastros.html', cadastros=cadastros, titulo ='Total de Cadastros')

@main.route('/cadastros/responsaveis')
@login_required
def lista_responsaveis():
    numero = Responsavel.query.count()
    responsaveis = Responsavel.query.order_by(Responsavel.nome).all()
    return render_template('lista_responsaveis.html',responsaveis=responsaveis, numero=numero)

@main.route('/cadastros/responsavel/<responsavel_id>')
@login_required
def dados_responsavel(responsavel_id,cadastro=None):
    responsavel = Responsavel.query.get(int(responsavel_id))
    total = Cadastro.query.filter(Cadastro.cpf.ilike('%'+ responsavel.cpf + '%')).count()
    cadastros = Cadastro.query.filter(Cadastro.cpf.ilike('%'+ responsavel.cpf + '%')).all()
    
   # numero=cadastro_numero
    # definir formulario para edição.
    return render_template('dados_responsavel.html',responsavel=responsavel, cadastros=cadastros,total=total)

@main.route('/cadastro/<cadastro_numero>')
@login_required
def cadastro_completo(cadastro_numero):
    cadastro = Cadastro.query.get(cadastro_numero)
    responsaveis=[]
    lista_cpf  = cadastro.cpf.split(';')
    for cpf in lista_cpf:
        responsavel = Responsavel.query.filter_by(cpf =cpf).first()
        if responsavel:
            responsaveis.append([responsavel.cpf,responsavel.nome,responsavel.id, responsavel.telefone, responsavel.email])
        
    # publisher_books = Book.query.filter_by(pub_id=publisher_id).all()
    return render_template('cadastro.html',cadastro=cadastro, cadastro_numero=cadastro.numero, responsaveis = responsaveis)

@main.route('/cadastrosud')
@login_required
def cadastros_unidade_geral():
    # total_por_ud=[]
    unidades = Unidades.query.order_by(Unidades.nome).all()
    cadastros = Cadastro.query.all()
    # for ud in unidades:
        # total = Cadastro.query.filter_by(unidade=ud.nome).count()
        # total_por_ud.append([ud,total]) 
    return render_template('lista_geral_unidades.html', unidades=unidades, cadastros = cadastros)
    # return render_template('lista_geral_unidades.html', unidades=total_por_ud)
   
    
@main.route('/cadastrosud/<unidade>')
@login_required
def cadastro_por_unidade(unidade):
    ud=unidade
    cadastros = Cadastro.query.filter_by(unidade=ud).all()
    # novo = sum(cadastros.modalidade.values('Cadastro Novo'))
    # adequa = sum(cadastros.modalidade.values('Adequacao'))
    # regula = sum(cadastros.modalidade.values('Regularização'))

    unidade=Unidades.query.filter_by(nome=ud).first()

    return render_template('lista_cadastros_unidade.html', cadastros=cadastros, unidade=unidade)


@main.route('/insere_cadastro/', methods=['GET', 'POST'])
@login_required
def insere_cadastro( ):
    if current_user.user_cat =='Conv':
        return redirect(url_for('authentication.acesso_negado'))
    
    #ajusta campos do formulario
    form = CriaCadastro()
    form.unidade.choices =[(None,'Selecione uma unidade')] + [(unidade.nome,unidade.nome) for unidade in Unidades.query.order_by(Unidades.nome).all()]
    form.aut_validade.data = None

    if form.validate_on_submit():
   
        usuario = current_user
        cpf = cria_lista(form.cpf.data) # lista de cpfs do campo de cpf do formulario
        lista_responsavel = cria_lista(form.responsavel.data) # lista de responsaveis do campo de responsaveis
        #verifica responsavel e adiciona na lista.
        for num in cpf:
            index = cpf.index(num)
            chave = Responsavel.query.filter_by(cpf=num).first()
            if not chave:
                responsavel = Responsavel(lista_responsavel[index], num, '','','') 
                db.session.add(responsavel)
               
        cadastro = Cadastro(
            numero = form.numero.data.upper(),
            unidade = form.unidade.data,
            acesso = form.acesso.data,
            titulo = form.titulo.data,
            data_cadastro = str(form.data_cadastro.data),
            situacao = form.situacao.data,
            cpf = lista_para_texto(cpf),
            modalidade = form.modalidade.data,
            finalidade = lista_para_texto(form.finalidade.data),
            aut_inst = form.aut_inst.data,
            aut_processo = form.aut_processo.data,
            aut_numero = form.aut_numero.data,
            aut_validade = form.aut_validade.data,
            curb = form.curb.data,
            data_inicio = form.data_inicio.data,
            data_fim = form.data_fim.data,
            membro_nome = tira_paragrafo(form.membro_nome.data),
            membro_instituicao = tira_paragrafo(form.membro_instituicao.data),
            componente_tipo = tira_paragrafo(form.componente_tipo.data),
            componente_especie = tira_paragrafo(form.componente_especie.data),
            raca_local = form.raca_local.data,
            envio_amostra = form.envio_amostra.data,
            cta = form.cta.data,
            componente_acessado = form.componente_acessado.data        
        )
        ## atualizar a tabela de atualizações!!!!
        db.session.add(cadastro)
        db.session.commit()
        
        atualizacao = AtualizacaoCadastro.atualiza_dados_cadastro(numero_cadastro = form.numero.data, tipo='Inclusão', id_usuario = usuario.id)

      
        flash(f'Cadastro {form.numero.data} adicionado com sucesso')
        return redirect(url_for('main.index'))
    
    return render_template('inserir_cadastro.html', form=form)

@main.route('/edita_cadastro/<cadastro_numero>', methods=['GET', 'POST'])
@login_required
def edita_cadastro(cadastro_numero):
    
    if current_user.user_cat =='Conv':
        return redirect(url_for('authentication.acesso_negado'))
    
    cadastro = Cadastro.query.get(cadastro_numero)
    #busca os responsaveis
    responsaveis=[]
    lista_cpf  = cria_lista_db(cadastro.cpf)
    for cpf in lista_cpf:
        responsavel = Responsavel.query.filter_by(cpf=cpf).first()
        if responsavel:
            responsaveis.append(responsavel)
    
    #ajusta os campos para serem exibidos
    form = EditaCadastroForm(obj=cadastro)
    form.unidade.choices = [(None,'Selecione uma unidade')] + [(unidade.nome,unidade.nome) for unidade in Unidades.query.order_by(Unidades.nome).all()]
    form.cpf.data = cria_texto_formulario(form.cpf.data)
    form.responsavel.data = '\n'.join([resp.nome for resp in responsaveis ])    
    form.membro_instituicao.data = cria_texto_formulario(form.membro_instituicao.data)
    form.membro_nome.data = cria_texto_formulario(form.membro_nome.data)
    form.componente_especie.data =  cria_texto_formulario(form.componente_especie.data)
    form.componente_tipo.data = cria_texto_formulario(form.componente_tipo.data)
  
    
    if form.validate_on_submit():

        usuario = current_user
        cpf = cria_lista(form.cpf.data) # lista de cpfs do campo de cpf do formulario
        lista_responsavel = cria_lista(form.responsavel.data) # lista de responsaveis do campo de responsaveis
        #verifica responsavel e adiciona na lista.
        for num in cpf:
            index = cpf.index(num)
            chave = Responsavel.query.filter_by(cpf=num).first()
            if not chave:
                responsavel = Responsavel(lista_responsavel[index], num, '','','') 
                db.session.add(responsavel)
        
        cadastro.unidade = form.unidade.data.upper()
        cadastro.acesso = form.acesso.data
        cadastro.titulo = form.titulo.data
        cadastro.data_cadastro = str(form.data_cadastro.data)
        cadastro.situacao = form.situacao.data
        cadastro.cpf = lista_para_texto(cpf)
        cadastro.modalidade = form.modalidade.data
        cadastro.finalidade = lista_para_texto(form.finalidade.data)
        cadastro.aut_inst = form.aut_inst.data
        cadastro.aut_processo = form.aut_processo.data
        cadastro.aut_numero = form.aut_numero.data
        cadastro.aut_validade = troca_por_nulo(form.aut_validade.data)
        cadastro.curb = form.curb.data
        cadastro.data_inicio = form.data_inicio.data
        cadastro.data_fim = form.data_fim.data
        cadastro.membro_nome = tira_paragrafo(form.membro_nome.data)
        cadastro.membro_instituicao = tira_paragrafo(form.membro_instituicao.data)
        cadastro.componente_tipo = tira_paragrafo(form.componente_tipo.data)
        cadastro.componente_especie = tira_paragrafo(form.componente_especie.data)
        cadastro.raca_local = form.raca_local.data
        cadastro.envio_amostra = form.envio_amostra.data
        cadastro.cta = form.cta.data
        cadastro.componente_acessado = form.componente_acessado.data

        db.session.add(cadastro)
        db.session.commit()

        atualizacao = AtualizacaoCadastro.atualiza_dados_cadastro(numero_cadastro = form.numero.data, tipo='Atualização',id_usuario = usuario.id)
       
        flash(f'Cadastro {form.numero.data} alterado com sucesso')
        return redirect(url_for('main.cadastro_completo', cadastro_numero = cadastro.numero))

    return render_template('edita_cadastro.html', form=form)


@main.route('/deleta_cadastro/<cadastro_numero>',  methods=['GET', 'POST'])
@login_required
def deleta_cadastro(cadastro_numero):

    if current_user.user_cat == 'Conv':
        flash(f'Você não tem permissão para excluir o cadastros')
        return redirect(url_for('main.index'))
    
    cadastro = Cadastro.query.get(cadastro_numero)
    
    if request.method == 'POST':
        usuario = current_user
        atualizacao = AtualizacaoCadastro.atualiza_dados_cadastro(numero_cadastro = cadastro.numero, tipo='Exclusão',id_usuario = usuario.id)
        db.session.delete(cadastro)
        db.session.commit()
        flash('Cadastro apagado com sucesso')
        return redirect(url_for('main.index'))
    return render_template('deleta_cadastro.html', cadastro = cadastro)


@main.route('/responsavel/<responsavel_id>', methods=['GET', 'POST'])
@login_required
def edita_responsavel(responsavel_id):

    responsavel = Responsavel.query.get(responsavel_id)
    form = ResponsavelForm(obj=responsavel)
    form.instituicao.choices =[(None,'Selecione uma unidade')] + [(unidade.nome,unidade.nome) for unidade in Unidades.query.order_by(Unidades.nome).all()]


    if form.validate_on_submit():
        responsavel.nome = form.nome.data
        responsavel.telefone = form.telefone.data
        responsavel.email = form.email.data
        responsavel.instituicao = form.instituicao.data

        db.session.add(responsavel)
        db.session.commit()

        flash('Cadastro alterado com sucesso')
        return redirect(url_for('main.lista_responsaveis'))
    return render_template('edita_responsavel.html',form=form, id = responsavel_id)

@main.route('/unidade/<unidade>', methods=['GET', 'POST'])
@login_required
def edita_unidade(unidade):

    unidade = Unidades.query.filter_by(nome=unidade).first()
    form = UnidadeForm(obj=unidade)
    lista_estados = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']
    form.estado.choices =[(None,'Selecione um estado')] + [(uf, uf) for uf in lista_estados]
   
    if form.validate_on_submit():
        unidade.cnpj = form.cnpj.data
        unidade.endereco = form.endereco.data
        unidade.cidade = form.cidade.data
        unidade.estado = form.estado.data
        unidade.cep = form.cep.data
        unidade.chefe_geral = form.chefe_geral.data
        unidade.telefone = form.telefone.data

        db.session.add(unidade)
        db.session.commit()

        flash('Dados alterados com sucesso')
        return redirect(url_for('main.cadastros_unidade_geral'))
    return render_template('edita_unidade.html',form=form, unidade=unidade)

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'SisAre.ico', mimetype='image/vnd.microsoft.icon')



