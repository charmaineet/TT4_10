from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL
import pymysql
import uuid

app = Flask(__name__)
CORS(app, support_credentials=True)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin123'
app.config['MYSQL_DATABASE_DB'] = 'loan_management'
app.config['MYSQL_DATABASE_HOST'] = 'dbshack-loan-database.cywxthrilvw1.ap-southeast-1.rds.amazonaws.com'
mysql.init_app(app)
conn = mysql.connect()
curr = conn.cursor()


# login endpoints

@app.route('/login')
@cross_origin(supports_credentials=True)
def login():
    return 'Login'


@app.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    # check if the user exists
    if not user or not check_password_hash(user.password, password):
        return 'Please check your login details and try again.'

    login_user(user)
    return 'Login successful'


@app.route('/signup')
@cross_origin(supports_credentials=True)
def signup():
    return 'Signup'


@app.route('/signup', methods=['POST'])
@cross_origin(supports_credentials=True)
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(login=email).first()
    if user:
        return 'Email address already exists'

    new_user = User(login=email, password=generate_password_hash(password, method='sha256'), name=name,
                    customerId=uuid.UUID4())
    db.session.add(new_user)
    db.session.commit()

    return 'Signup successful'


@app.route('/logout')
@cross_origin(supports_credentials=True)
def logout():
    logout_user()
    return 'Logout successful'


# endpoints to get loans/balances
@app.route('/customer', methods=['GET'])
@cross_origin(supports_credentials=True)
def customer_get():
    if len(request.args) > 1:
        return jsonify({
                           'message': 'sorry please input one query parameter at a time or the api will only fulfil the criteria of the last query parameter'})

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


@app.route('/loan', methods=['GET'])
@cross_origin(supports_credentials=True)
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


@app.route('/customer', methods=['PUT'])
@cross_origin(supports_credentials=True)
def customer_put():
    parameters = {
        'CustomerId': '\'None\'',
        'customer_name': '\'None\'',
        'customer_phone': '\'None\'',
        'customer_address': '\'None\'',
        'balance': '\'None\''
    }
    parameter_names = ['CustomerId', 'customer_name', 'customer_phone', 'customer_address', 'balance']
    for param in range(len(parameter_names)):
        if parameter_names[param] in request.args:
            parameters[parameter_names[param]] = request.args[parameter_names[param]]
        else:
            return f'{parameter_names[param]} not found'
    try:
        curr.execute(
            'INSERT INTO customer VALUES (\'{0}\',\'{1}\',\'{2}\', \'{3}\', \'{4}\')'.format(parameters['CustomerId'],
                                                                                             parameters[
                                                                                                 'customer_name'],
                                                                                             parameters[
                                                                                                 'customer_phone'],
                                                                                             parameters[
                                                                                                 'customer_address'],
                                                                                             parameters['balance']))
        conn.commit()
    except pymysql.err.IntegrityError:
        return jsonify({'message': 'duplicate primary key'})

    return jsonify({'message': 'Posted'})


@app.route('/loan', methods=['PUT'])
@cross_origin(supports_credentials=True)
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
        curr.execute(
            'INSERT INTO loan VALUES (\'{0}\',\'{1}\')'.format(parameters['LoanId'], parameters['loan_amount']))
        conn.commit()
    except pymysql.err.IntegrityError:
        return jsonify({'message': 'duplicate primary key'})

    return jsonify({'message': 'Posted'})


@app.route('/customer/update_balance', methods=['PATCH'])
@cross_origin(supports_credentials=True)
def customer_patch_balance():
    if 'CustomerId' in request.args:
        curr.execute('UPDATE customer SET balance = \'{0}\' WHERE CustomerId = \'{1}\''.format(request.args['balance'],
                                                                                               request.args[
                                                                                                   'CustomerId']))
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
@cross_origin(supports_credentials=True)
def customer_patch_phone():
    if 'CustomerId' in request.args:
        curr.execute('UPDATE customer SET customer_phone = \'{0}\' WHERE CustomerId = \'{1}\''.format(
            request.args['customer_phone'], request.args['CustomerId']))
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
@cross_origin(supports_credentials=True)
def customer_patch_address():
    if 'CustomerId' in request.args:

        curr.execute('UPDATE customer SET customer_address = \'{0}\' WHERE CustomerId = \'{1}\''.format(
            request.args['customer_address'], request.args['CustomerId']))

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
@cross_origin(supports_credentials=True)
def loan_patch_loan_amount():
    if 'LoanId' in request.args:

        curr.execute('UPDATE loan SET loan_amount = \'{0}\' WHERE LoanId = \'{1}\''.format(request.args['loan_amount'],
                                                                                           request.args['LoanId']))

        curr.execute('SELECT * FROM loan WHERE LoanId = \'{0}\''.format(request.args['LoanId']))
        updated_modules = curr.fetchall()
        conn.commit()
        return 'Updated!' + str(updated_modules)
    else:
        if 'LoanId' not in request.args:
            return jsonify({'message': 'Loan Id not sent'})
        else:
            return jsonify({'message': 'loan_amount not sent'})


@app.route('/customer/deletebyid', methods=['DELETE'])
@cross_origin(supports_credentials=True)
def customer_delete():
    if 'CustomerId' in request.args:

        curr.execute('DELETE FROM customer WHERE CustomerId = \'{0}\''.format(request.args['CustomerId']))
        conn.commit()
        return jsonify({'message': 'Deleted!'})


    else:
        return jsonify({'message': ' no customer id provided'})


@app.route('/loan/deletebyid', methods=['DELETE'])
@cross_origin(supports_credentials=True)
def loan_delete():
    if 'LoanId' in request.args:

        curr.execute('DELETE FROM loan WHERE LoanId = \'{0}\''.format(request.args['LoanId']))
        conn.commit()
        return jsonify({'message': 'Deleted!'})


    else:
        return jsonify({'message': ' no customer id provided'})


@app.route('/customerloan', methods=['GET'])
@cross_origin(supports_credentials=True)
def customer_loan_get():
    curr.execute(
        "SELECT customer_name,SUM(loan_amount) FROM customer INNER JOIN customerloan ON customer.CustomerId=customerloan.CustomerId INNER JOIN loan on customerloan.LoanId = loan.LoanId WHERE customer.CustomerId = \'{0}\'".format(
            request.args['CustomerId']))

    sql_modules = curr.fetchall()
    return jsonify(sql_modules)


app.run(debug=True, host='0.0.0.0')