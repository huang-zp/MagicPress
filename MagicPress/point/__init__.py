from flask import Blueprint

point = Blueprint('point', __name__)

from . import views