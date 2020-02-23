from flask import Blueprint
routes = Blueprint('routes', __name__)
from register_database_api.routes.employee_api import *