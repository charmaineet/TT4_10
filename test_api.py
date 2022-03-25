from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
import pymysql


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
def customer_get():
    if len(request.args) > 1:
        return jsonify({'message': 'sorry please input one query parameter at a time or the api will only fulfil the criteria of the last query parameter'})

    parameter_list = ['CustomerId', 'customer_name', 'customer_phone', 'customer_address', 'balance']

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
def loan_get():

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
    try:
        curr.execute('INSERT INTO customer VALUES (\'{0}\',\'{1}\',\'{2}\', \'{3}\', \'{4}\')'.format(parameters['CustomerId'],parameters['customer_name'], parameters['customer_phone'], parameters['customer_address'], parameters['balance']))
        conn.commit()
    except pymysql.err.IntegrityError:
        return jsonify({'message': 'duplicate primary key'})

    return jsonify({'message':'Posted'})


@app.route('/loan', methods = ['PUT'])
def loan_put():
    
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
    try:
        curr.execute('INSERT INTO loan VALUES (\'{0}\',\'{1}\')'.format(parameters['LoanId'],parameters['loan_amount']))
        conn.commit()
    except pymysql.err.IntegrityError:
        return jsonify({'message': 'duplicate primary key'})

    return jsonify({'message':'Posted'})


@app.route('/customer/update_balance', methods=['PATCH'])

def customer_patch_balance():

    if 'CustomerId' in request.args:
        curr.execute('UPDATE customer SET balance = \'{0}\' WHERE CustomerId = \'{1}\''.format(request.args['balance'], request.args['CustomerId']))
        curr.execute('SELECT * FROM customer WHERE CustomerId = \'{0}\''.format(request.args['CustomerId']))
        updated_modules = curr.fetchall()
        conn.commit()
        return 'Updated!' + str(updated_modules)
    else:
        if 'CustomerId' not in request.args:
            return 'Customer Id not sent'
        else:
            return 'Balance not sent'



@app.route('/customer/update_phone', methods=['PATCH'])

def customer_patch_phone():

    if 'CustomerId' in request.args:
        curr.execute('UPDATE customer SET customer_phone = \'{0}\' WHERE CustomerId = \'{1}\''.format(request.args['customer_phone'], request.args['CustomerId']))
        curr.execute('SELECT * FROM customer WHERE CustomerId = \'{0}\''.format(request.args['CustomerId']))
        updated_modules = curr.fetchall()
        conn.commit()
        return 'Updated!' + str(updated_modules)
    else:
        if 'CustomerId' not in request.args:
            return 'Customer Id not sent'
        else:
            return 'customer_phone not sent'

@app.route('/customer/update_address', methods=['PATCH'])

def customer_patch_address():

    if 'CustomerId' in request.args:

        curr.execute('UPDATE customer SET customer_address = \'{0}\' WHERE CustomerId = \'{1}\''.format(request.args['customer_address'], request.args['CustomerId']))

        curr.execute('SELECT * FROM customer WHERE CustomerId = \'{0}\''.format(request.args['CustomerId']))
        updated_modules = curr.fetchall()
        conn.commit()
        return 'Updated!' + str(updated_modules)
    else:
        if 'CustomerId' not in request.args:
            return 'Customer Id not sent'
        else:
            return jsonify({'message': 'customer_address not sent'})

@app.route('/loan/update_amount', methods=['PATCH'])
def loan_patch_loan_amount():

    if 'LoanId' in request.args:

        curr.execute('UPDATE loan SET loan_amount = \'{0}\' WHERE LoanId = \'{1}\''.format(request.args['loan_amount'], request.args['LoanId']))

        curr.execute('SELECT * FROM loan WHERE LoanId = \'{0}\''.format(request.args['LoanId']))
        updated_modules = curr.fetchall()
        conn.commit()
        return 'Updated!' + str(updated_modules)
    else:
        if 'LoanId' not in request.args:
            return jsonify({'message':'Loan Id not sent'})
        else:
            return jsonify({'message': 'loan_amount not sent'})




@app.route('/customer/deletebyid', methods = ['DELETE'])
def customer_delete():
    if 'CustomerId' in request.args:

        curr.execute('DELETE FROM customer WHERE CustomerId = \'{0}\''.format(request.args['CustomerId']))
        conn.commit()
        return jsonify({'message':'Deleted!'})


    else:
        return jsonify({'message':' no customer id provided'})

@app.route('/loan/deletebyid', methods = ['DELETE'])
def loan_delete():
    if 'LoanId' in request.args:

        curr.execute('DELETE FROM loan WHERE LoanId = \'{0}\''.format(request.args['LoanId']))
        conn.commit()
        return jsonify({'message':'Deleted!'})


    else:
        return jsonify({'message':' no customer id provided'})


@app.route('/customerloan', methods = ['GET'])
def customer_loan_get():


    curr.execute("SELECT customer_name,SUM(loan_amount) FROM customer INNER JOIN customerloan ON customer.CustomerId=customerloan.CustomerId INNER JOIN loan on customerloan.LoanId = loan.LoanId WHERE customer.CustomerId = \'{0}\'".format(request.args['CustomerId']))

    sql_modules = curr.fetchall()
    return jsonify(sql_modules)

app.run(debug=True)