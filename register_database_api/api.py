""" REST API Module

This module provides the main interface between the backend postgres database. The flask API currently
runs on port 5000 and provides data to clients from the database.

Example:
    Start up the flask API on your local computer. An example query to the database is as follows:
    http://127.0.0.1:5000/api/v1/resources/products?lookup=lookupcode1



Attributes:
    DATABASE_URL is a local environment variable that contains the value of the postgres database uri.


"""
import flask
from flask_cors import CORS
import os
import routes

app = flask.Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config["DEBUG"] = True
app.register_blueprint(routes.employee_api)
app.register_blueprint(routes.transaction_api)
app.register_blueprint(routes.product_api)

@app.errorhandler(404)
def page_not_found(e):
    """ When client connects to a route that doesn't exist.

    Returns: Error message that resource was not found.
    """
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
