from flask import Blueprint, request, jsonify, abort
import psycopg2
import os
import uuid
from random import randint

transaction_api = Blueprint('transaction_api', __name__)

DATABASE_URL = os.environ['DATABASE_URL']

def parse_transaction_info(record_list):
    data_list = []
    for record in record_list:
        data_record = {
            "id": record[0],
            "transactionid": record[1],
            "cashierid": record[2],
            "transactiontotal": str(record[3]),
            "totalproductcount": record[4],
            "productspurchased": record[5]
        }
        data_list.append(data_record)
    return data_list

def create_transaction_object(record):
    data_record = {
        "transactionid": str(randint(0,100000000)),
        "cashierid": record["cashierid"],
        "transactiontotal": str(record["transactiontotal"]),
        "totalproductcount": record["totalproductcount"],
        "productspurchased": record["productspurchased"]
    }
    return data_record

@transaction_api.route("/api/v1/transaction/all")
def transaction_list():
    """
        Responds with a JSON list of all transactions
    """
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transaction")
    record_list = cursor.fetchall()
    conn.close()
    data_list = parse_transaction_info(record_list)
    return jsonify(data_list)

@transaction_api.route("/api/v1/transaction")
def transaction_filter():
    """
        Request a specific transaction
            ?transactionid=<transactionid>
        Returns JSON representation of transaction
    """
    query_parameters = request.args
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    lookup_code = query_parameters.get('transactionid')
    base_query = "SELECT * FROM transaction WHERE"
    if lookup_code:
        query = "{} transactionid='{}'".format(base_query,lookup_code)
        cursor.execute(query)
        record_list = cursor.fetchall()
        conn.close
        data_list = parse_transaction_info(record_list)
        return jsonify(data_list)
    else:
        conn.close()
        return "<h1>404</h1><p>The transactionid was not found.</p>"

@transaction_api.route("/api/v1/transaction/create", methods=['POST'])
def transaction_create():
    """
    Create transaction
    Args:
        {
            "cashierid": 123,
            "productspurchased":[
                'lookupcode1',
                'lookupcode2'
            ]
            "totalproductscount": 5,
            "transactiontotal": 25.42
        }
    """
    if not request.json:
            abort(400)
    conn = psycopg2.connect(DATABASE_URL,sslmode='require')
    cursor = conn.cursor()
    record = create_transaction_object(request.json)
    query = """INSERT INTO transaction(transactionid,cashierid,transactiontotal,totalproductcount,productspurchased)
    VALUES('{}','{}','{}','{}',ARRAY{});"""
    try:
        insert_query = query.format(
            record["transactionid"],
            record["cashierid"],
            record["transactiontotal"],
            record["totalproductcount"],
            record["productspurchased"])
        cursor.execute(insert_query)
        conn.commit()
    finally:
        conn.close()
    return jsonify(record),201

@transaction_api.route("/api/v1/transaction/delete", methods=['POST'])
def transaction_delete():
    """
    Transaction deletion
    Args:
        {
            "id":<transactionid>
        }
    """
    if not request.json or not 'id' in request.json:
        abort({'message':'Invalid query, expecting {"id":<transactionid>}'}, 400)
    record = {
        "id":request.json["id"]
    }
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    base_query = "DELETE FROM transaction WHERE transactionid={}"
    try:
        delete_query = base_query.format(record["id"])
        cursor.execute(delete_query)
        conn.commit()
    finally:
        conn.close()
    return jsonify({"status":"success"}),201

@transaction_api.route("/api/v1/transaction/update",methods=['POST'])
def transaction_update():
    """Transaction update
    Args:
        {
            "cashierid": 123,
            "productspurchased":[
                'lookupcode1',
                'lookupcode2'
            ]
            "totalproductscount": 5,
            "transactionid": 123456
            "transactiontotal": 25.42
        }"""
    if not request.json:
        abort(400)
    conn = psycopg2.connect(DATABASE_URL,sslmode='require')
    cursor = conn.cursor()
    record = create_transaction_object(request.json)
    query = """UPDATE transaction
            SET cashierid = '{}',
                transactiontotal = '{}',
                totalproductcount = '{}',
                productspurchased = ARRAY{}
            WHERE transactionid = '{}'"""
    try:
        update_query = query.format(
            record["cashierid"],
            record["transactiontotal"],
            record["totalproductcount"],
            record["productspurchased"],
            request.json["transactionid"]
        )
        cursor.execute(update_query)
        conn.commit()
    finally:
        conn.close()
    return jsonify({"status": "success"}),201
