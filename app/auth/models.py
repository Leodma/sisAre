# user model

from datetime import datetime
from app import db, bcrypt # app/__init__.py
from flask_login import UserMixin
from app import login_manager

class User(UserMixin,db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20))
    user_email = db.Column(db.String(60), unique=True, index=True)
    user_password = db.Column(db.String(80))
    user_cat = db.Column(db.String(20))
    registration_date = db.Column(db.DateTime, default=datetime.now)
    atualizacao = db.relationship('AtualizacaoCadastro', backref='activeuser', lazy='dynamic')

    

    def check_password(self,password): # função para checar se a senha está correta
        return bcrypt.check_password_hash(self.user_password, password)


    # classmethod não é associado a instância, é utilizado pela classe em si.
    @classmethod
    def create_user(cls, user, email, nivel, password): # - CLS é a classe passada como parametro.
        user = cls( user_name=user,
                    user_email = email,
                    user_cat = nivel,
                    user_password = bcrypt.generate_password_hash(password).decode('utf-8')
                    )
        db.session.add(user)
        db.session.commit()
        return user

    
    def retorna_data(self,data):
        return data.strftime("%d-%b-%Y")

    
    def altera_senha(self, password):
        self.user_password = bcrypt.generate_password_hash(password).decode('utf-8')
        return 


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))