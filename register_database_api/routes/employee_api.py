from flask import Blueprint, request, jsonify, abort
import psycopg2
import os
import uuid
from random import randint

employee_api = Blueprint('employee_api', __name__)

DATABASE_URL = os.environ['DATABASE_URL']


def parse_employee_info(record_list):
    """ Parses the employee record information

    Example input:
    [('3c7ca263-9383-4d61-b507-2c8bd367567f', 123456, 'Austin', 'Grover', <memory at 0x11059def0>, True, 1,
     '00000000-0000-0000-0000-000000000000', datetime.datetime(2020, 2, 23, 16, 53, 25, 531305))]

    Args:
        Employee Record list

    Returns:
        list of dictionary records containing employee information.

    """
    data_list = []
    for record in record_list:
        user_password = memoryview(record[4]).tobytes().decode("utf-8")
        data_record = {
            "id": record[0],
            "employeeid": record[1],
            "firstname": record[2],
            "lastname": record[3],
            "password": user_password,
            "active": record[5],
            "classification": record[6],
            "managerid": record[7],
            "createdon": record[8],
        }
        data_list.append(data_record)
    return data_list


def create_employee_object(record):
    data_record = {
        "employeeid": str(randint(0, 100000000)),
        "firstname": record["firstname"],
        "lastname": record["lastname"],
        "password": record["password"],
        "active": record["active"],
        "classification": record["classification"],
        "managerid": record["managerid"]
    }

    return data_record


@employee_api.route("/api/v1/employee/all")
def employee_list():
    """ Method that responds with a JSON list of employees contained in the employee table.

    Returns:
        jsonify: An array of json objects representing each record in the database.

    """
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee")
    record_list = cursor.fetchall()
    conn.close()
    data_list = parse_employee_info(record_list)

    return jsonify(data_list)


@employee_api.route("/api/v1/employee")
def filter_employee():
    """ When the client requests a specific employee.
    Valid queries:
         ?employeeid=<employeeid>

    Returns: json representation of product.

    """
    query_parameters = request.args
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    lookup_code = query_parameters.get('employeeid')

    base_query = "SELECT * FROM employee WHERE"
    if lookup_code:
        query = "{} employeeid = '{}'".format(base_query, lookup_code)
        cursor.execute(query)
        record_list = cursor.fetchall()
        conn.close()
        data_list = parse_employee_info(record_list)
        return jsonify(data_list)
    else:
        conn.close()
        return "<h1>404</h1><p>The employeeid was not found.</p>"


@employee_api.route("/api/v1/employee/create", methods=['POST'])
def create_employee():
    """ REST API for product creation

    Args:
      {
        "active": true,
        "classification": 3,
        "firstname": "Colton",
        "lastname": "Tucker",
        "managerid": "8c460ba4-6358-4a78-9493-850ab8c43545", or  "managerid": ""
        "password": "coltonboss433"
      }

    Returns:
        JSON object of record that was created, HTTP Status Code 201
          {
            "active": true,
            "classification": 3,
            "createdon": "Sun, 23 Feb 2020 16:59:39 GMT",
            "employeeid": 123444,
            "firstname": "Colton",
            "id": "49d8b5af-97b4-4ae9-b38b-2df3e9173c93",
            "lastname": "Tucker",
            "managerid": "8c460ba4-6358-4a78-9493-850ab8c43545",
            "password": "coltonboss433"
          }
        Raises:
        Exception error if unable to connect
    """
    if not request.json or not 'classification' in request.json:
        abort(400)
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    record = create_employee_object(request.json)
    print("Record looks like {}".format(record))

    with_manager_query = """INSERT INTO employee(employeeid, firstname, lastname, password, active, classification, managerid)
    VALUES
       ('{}','{}','{}','{}','{}','{}','{}');
    """

    without_manager_query = """INSERT INTO employee(employeeid, firstname, lastname, password, active, classification)
     VALUES
        ('{}','{}','{}','{}','{}','{}');
     """


    try:
        if record["managerid"] == '':
            insert_query = without_manager_query.format(
                record["employeeid"],
                record["firstname"],
                record["lastname"],
                record["password"],
                record["active"],
                record["classification"])
            cursor.execute(insert_query)
            conn.commit()
        else:
            insert_query = with_manager_query.format(
                record["employeeid"],
                record["firstname"],
                record["lastname"],
                record["password"],
                record["active"],
                record["classification"],
                record["managerid"])
            cursor.execute(insert_query)
            conn.commit()
    finally:
        conn.close()
    return jsonify(record), 201


@employee_api.route('/api/v1/employee/delete', methods=['POST'])
def employee_delete():
    """ REST API for employee deletion

    Args:
        {"id":<record_id>}

    Returns:
        JSON object of record that was created, HTTP Status Code 201
        Following is an example response
        {
            "status": "succeeded",

        }
    Raises:
        Exception error if unable to delete or invalid requestå
    """
    if not request.json or not 'id' in request.json:
        abort({'message': 'Invalid query, expecting: {"id":<employee_id>}'}, 400)
    record = {
        "id": request.json["id"],
    }

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    base_query = "DELETE FROM employee WHERE id ='{}'"

    try:
        insert_query = base_query.format(record["id"])
        cursor.execute(insert_query)
        conn.commit()
    finally:
        conn.close()
    return jsonify({"status": "succeeded"}), 201


@employee_api.route('/api/v1/employee/update', methods=['POST'])
def employee_update():
    """ REST API for employee updates

    Args:
        {"id":<record_id>}

    Returns:
        JSON object of record that was created, HTTP Status Code 201
        Following is an example response
        {
            "status": "succeeded",

        }
    Raises:
        Exception error if unable to delete or invalid requestå
    """
    if not request.json or not 'id' in request.json:
        abort({'message': 'Invalid query, expecting: {"id":<employee_id>}'}, 400)
    record = {
        "id": request.json["id"],
    }

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    base_query = "DELETE FROM employee WHERE id ='{}'"

    try:
        insert_query = base_query.format(record["id"])
        cursor.execute(insert_query)
        conn.commit()
    finally:
        conn.close()
    return jsonify({"status": "succeeded"}), 201
