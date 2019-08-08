# app/tc/__init__.py
from flask import Blueprint

buscar = Blueprint('buscar',__name__, template_folder='templates')

from app.busca import routes