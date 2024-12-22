from flask import Blueprint

announce_blueprint = Blueprint('announce', __name__, url_prefix='/announce')

from . import views