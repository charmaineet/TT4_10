from flask import Flask, request, jsonify
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin123'
app.config['MYSQL_DATABASE_DB'] = 'loan_management'
app.config['MYSQL_DATABASE_HOST'] = 'dbshack-loan-database.cywxthrilvw1.ap-southeast-1.rds.amazonaws.com'
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




@app.route('/customer', methods = ['PUT'])
def customer_put():
    # module_code, module_title,module_instructor, module_credits = '', '', '', 0
    parameters = {
        'CustomerId': '\'None\'',
        'customer_name': '\'None\'',
        'customer_phone': '\'None\'',
        'customer_address': '\'None\'',
        'balance':'\'None\''
    }
    parameter_names = ['CustomerId','customer_name', 'customer_phone', 'customer_address', 'balance']
    for param in range(len(parameter_names)):
        if parameter_names[param] in request.args:
            parameters[parameter_names[param]] = request.args[parameter_names[param]]
        else:
            return f'{parameter_names[param]} not found'



    # print('INSERT INTO customer VALUES (\'{0}\',\'{1}\',\'{2}\', \'{3}\')'.format(parameters['customer_name'], parameters['customer_phone'], parameters['customer_address']))
    curr.execute('INSERT INTO customer VALUES (\'{0}\',\'{1}\',\'{2}\', \'{3}\', \'{4}\')'.format(parameters['CustomerId'],parameters['customer_name'], parameters['customer_phone'], parameters['customer_address'], parameters['balance']))

    conn.commit()
    return 'Posted'


@app.route('/loan', methods = ['PUT'])
def loan_put():
    # module_code, module_title,module_instructor, module_credits = '', '', '', 0
    parameters = {
        'LoanId': '\'None\'',
        'loan_amount': '\'None\''
    }
    parameter_names = ['LoanId', 'loan_amount']
    for param in range(len(parameter_names)):
        if parameter_names[param] in request.args:
            parameters[parameter_names[param]] = request.args[parameter_names[param]]
        else:
            return f'{parameter_names[param]} not found'



    # print('INSERT INTO customer VALUES (\'{0}\',\'{1}\',\'{2}\', \'{3}\')'.format(parameters['customer_name'], parameters['customer_phone'], parameters['customer_address']))
    curr.execute('INSERT INTO loan VALUES (\'{0}\',\'{1}\')'.format(parameters['LoanId'],parameters['loan_amount']))

    conn.commit()
    return 'Posted'


app.run(debug=True)