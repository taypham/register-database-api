from flask import Blueprint
routes = Blueprint('routes', __name__)
from routes.employee_api import *
from routes.transaction_api import *
from routes.product_api import *