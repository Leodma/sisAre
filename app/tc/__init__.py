# app/tc/__init__.py
from flask import Blueprint

termos = Blueprint('termos',__name__, template_folder='templates')

from app.tc import routes