from flask import Flask, request, jsonify
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'loan_management'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
curr = conn.cursor()


@app.route('/customer', methods = ['GET'])
def customer_all():

    parameter_list = ['customer_name', 'customer_phone', 'customer_address']

    for params in parameter_list:
        print(params)
        if params in request.args:
            curr.execute('SELECT * FROM customer WHERE {0} = \'{1}\''.format(params, request.args[params]))

            filtered_result = curr.fetchall()
            return jsonify(filtered_result)

    curr.execute('SELECT * FROM customer')
    sql_modules = curr.fetchall()
    return jsonify(sql_modules)


@app.route('/loan', methods = ['GET'])
def loan_all():

    parameter_list = ['loanId', 'loan_amount']

    for params in parameter_list:
        print(params)
        if params in request.args:
            curr.execute('SELECT * FROM loan WHERE {0} = \'{1}\''.format(params, request.args[params]))

            filtered_result = curr.fetchall()
            return jsonify(filtered_result)

    curr.execute('SELECT * FROM loan')
    sql_modules = curr.fetchall()
    return jsonify(sql_modules)
