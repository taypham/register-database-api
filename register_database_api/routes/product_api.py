from flask import Blueprint, request, jsonify, abort
import os
import psycopg2
import uuid
import datetime

product_api = Blueprint('product_api', __name__)

DATABASE_URL = os.environ['DATABASE_URL']

@product_api.route('/api/v1/products/all', methods=['GET'])
def api_all():
    """ Method that responds with a JSON list of records contained in the product table.

    Returns:
        jsonify: An array of json objects representing each record in the dat®abase.

    """
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product")
    record_list = cursor.fetchall()
    conn.close()
    data_list = []
    for record in record_list:
        data_record = {
            "id": record[0],
            "lookup_code": record[1],
            "count": record[2],
            "creation": record[3],
            "price": record[4]
        }
        data_list.append(data_record)

    return jsonify(data_list)


@product_api.route('/api/v1/products/delete', methods=['POST'])
def product_delete():
    """ REST API for product deletion

    Args:
        {"id":<product_id>, "lookup_code": <lookup_code>}

    Returns:
        JSON object of record that was created, HTTP Status Code 201
        Following is an example response
        {
            "status": "succeeded",

        }
    Raises:
        Exception error if unable to delete or invalid requestå
    """
    if not request.json or not 'lookup_code' in request.json:
        abort({'message': 'Invalid query, expecting: {"id":<product_id>, "lookup_code": <lookup_code>}'}, 400)
    record = {
        "id": request.json["id"],
        "lookup_code": request.json["lookup_code"],
    }

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    base_query = "DELETE FROM product WHERE id ='{}' and LookupCode ='{}'"

    try:
        insert_query = base_query.format(record["id"], record['lookup_code'])
        cursor.execute(insert_query)
        conn.commit()
    finally:
        conn.close()
    return jsonify({"status": "succeeded"}), 201


@product_api.route('/api/v1/products/create', methods=['POST'])
def product_create():
    """ REST API for product creation

    Args:
        {"lookup_code":<lookup_code>,"count":<product_count>}

    Returns:
        JSON object of record that was created, HTTP Status Code 201

        Following is an example response
        {
          "count": "400",
          "creation": "Wed, 19 Feb 2020 23:41:15 GMT",
          "id": "9c90e37a-53a3-11ea-a78b-acde48001122",
          "lookup_code": "lookupcode4",
          "price":100
        }

    Raises:
        Exception error if unable to connect

    """
    if not request.json or not 'lookup_code' in request.json:
        abort(400)
    record = {
        "id": uuid.uuid1(),
        "lookup_code": request.json["lookup_code"],
        "count": request.json["count"],
        "creation": datetime.datetime.now(),
        "price": request.json["price"]
    }

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    base_query = "INSERT INTO product(id,LookupCode,Count,Createdon,price) VALUES ('{}','{}', '{}','{}','{}')"

    try:
        insert_query = base_query.format(record["id"], record['lookup_code'], record['count'], record['creation'], record['price'])
        cursor.execute(insert_query)
        conn.commit()
    finally:
        conn.close()
    return jsonify(record), 201


@product_api.route('/api/v1/products', methods=['GET'])
def product_filter():
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
            "lookup_code": record[0][1],
            "count": record[0][2],
            "creation": record[0][3],
            "price": record[0][4]
        }
        return jsonify(record)
    else:
        return "<h1>404</h1><p>The lookup id was not found.</p>"