from app import create_app, db
from app.auth.models import User
from sqlalchemy import exc

# remova a linha abaixo para rodar localmente
# if __name__ == "__main__":
flask_app = create_app('prod')
    
with flask_app.app_context():
    db.create_all()
    try:
        if not  User.query.filter_by(user_name='leo').first():
            User.create_user(user='Leo', email = 'leodma@gmail.com', nivel='Adm', password = 'leo123')
    except exc.IntegrityError:
        flask_app.run()