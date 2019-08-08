from app import create_app,db
from app.auth.models import User

# remova a linha abaixo para rodar localmente
# if __name__ == "__main__":
    flask_app = create_app('prod')
    
    with flask_app.app_context():
        db.create_all()

        # if not User.query.filter_by(user_name='annathais').first():
        #     User.create_user(user='annathais',email='annathais@embrapa.br', password='klgmd2331')

    
    flask_app.run()