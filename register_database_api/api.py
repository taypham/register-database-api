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
from flask import request, jsonify
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/v1/products/all', methods=['GET'])
def api_all():
    """ Method that responds with a JSON list of records contained in the product table.

    Returns:
        jsonify: An array of json objects representing each record in the database.

    """
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product")
    record_list = cursor.fetchall()
    data_list = []
    for record in record_list:
        data_record = {
            "id": record[0],
            "lookup-code":record[1],
            "count": record[2],
            "creation": record[3]
        }
        data_list.append(data_record)

    return jsonify(data_list)


@app.errorhandler(404)
def page_not_found(e):
    """ When client connects to a route that doesn't exist.

    Returns: Error message that resource was not found.
    """
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/products', methods=['GET'])
def api_filter():
    """ When the client requests a specific product.
    Valid queries:
         ?lookup=<lookupcode>

    Returns: json representation of product.

    """
    query_parameters = request.args
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    lookup_code = query_parameters.get('lookup')

    base_query = "SELECT * FROM product WHERE"

    if lookup_code:
        query = "{} Lookupcode = '{}'".format(base_query, lookup_code)
        cursor.execute(query)
        record = cursor.fetchall()
        print(record)
        print(type(record))
        record = {
            "id": record[0][0],
            "lookup-code": record[0][1],
            "count": record[0][2],
            "creation": record[0][3]
        }
        return jsonify(record)
    else:
        return "<h1>404</h1><p>The lookup id was not found.</p>"


app.run()
