# app/__init__.py

import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'authentication.do_the_login'
login_manager.session_protection = 'strong'
bcrypt = Bcrypt()

def page_not_found(e):
    return render_template('error404.html'), 404

def create_app(config_type): # dev, test ou prod
    app = Flask(__name__)
    configuration = os.path.join(os.getcwd(),'config', config_type + '.py')
    app.config.from_pyfile(configuration)
    app.register_error_handler(404, page_not_found)
    
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app.cadastros import main  #caminho para app/cadastros
    app.register_blueprint(main)

    from app.auth import authentication
    app.register_blueprint(authentication)

    from app.tc import termos
    app.register_blueprint(termos)

    from app.busca import buscar
    app.register_blueprint(buscar)
   

    return app
