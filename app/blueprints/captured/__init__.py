from flask import Blueprint

captured = Blueprint('captured', __name__, template_folder='captured_templates')

from . import routes