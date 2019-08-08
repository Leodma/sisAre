from app import create_app,db
from app.auth.models import User
from sqlalchemy import exc


# remova a linha abaixo para rodar localmente
# if __name__ == "__main__":
flask_app = create_app('prod')
    
with flask_app.app_context():
    db.create_all()
    try:
        if not User.query.filter_by(user_email="teste").first():
            User.create_user(user='teste', email = 'teste@teste.com.br', nivel = 'Conv', password =  't&st&sisare')
    except exc.IntegrityError():
        flask_app.run()