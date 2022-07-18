from pprint import pprint
import requests
import googlemaps
import os
import pandas as pd
import sqlalchemy as db
from flask import Flask, jsonify, request, render_template
from sqlalchemy import text
from sqlalchemy import create_engine, MetaData, Table, Column, Integer
from sqlalchemy.orm import Session, registry
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = db.create_engine('sqlite:///buy_sell_database.sql')

meta = MetaData()
meta.reflect(bind=engine, views=True)
mapper_registry = registry()
inspector = db.inspect(engine)
if not inspector.has_table("user"):
    engine.execute(
        "CREATE TABLE `user` ("
        "`user_id` INTEGER NOT NULL PRIMARY KEY,"
        "`user_name` TEXT NOT NULL,"
        "`user_email` TEXT NOT NULL,"
        "`user_phone_number` TEXT NOT NULL,"
        "`user_address` TEXT NOT NULL,"
        "`user_password` TEXT NOT NULL"
        ")")
    # engine.execute(f"INSERT INTO game (id) VALUES (1);")

if not inspector.has_table("item"):
    engine.execute(
        "CREATE TABLE `item` ("
        "`item_id` INTEGER NOT NULL PRIMARY KEY,"
        "`item_name` TEXT NOT NULL,"
        "`item_price` TEXT NOT NULL,"
        "`item_description` TEXT NOT NULL,"
        "`seller_id` INTEGER NOT NULL,"
        "FOREIGN KEY (`seller_id`)"
        "   REFERENCES user (user_id)"
        ")")

app = Flask(__name__)

session = Session(engine)


# raw query
@app.route('/<table_name>')
def get_table_data(table_name: str):
    if table_name in meta.tables:
        print('legal')
    else:
        print('illegal table')
        return jsonify([])
    results = session.execute(text('select * from {}'.format(table_name)))
    data = []
    for r in results:
        data.append(dict(r))
    return jsonify(data)


@app.route('/<table_name>/<int:id>')
def get_resource_by_pk(table_name: str, id: int):
    if table_name in meta.tables:
        print('legal')
    else:
        print('illegal table')
        return jsonify({})
    pk = ''
    cols = meta.tables[table_name].columns
    for c in cols:
        if c.primary_key:
            pk = c.name
    results = session.execute(text('select * from {} where {}={}'.format(table_name, pk, id)))
    data = []
    for r in results:
        data.append(dict(r))
    return jsonify(data)


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', 'default value email')
        password = request.form.get('password', 'default value password')
        print('email: ' + email)
        print('password: ' + password)
        try:
            connection = engine.connect()
            cursor = connection.execute("SELECT user_password from user where user_email=?;", (email))
            result = cursor.scalar()
            print(result)
            print(type(result))
            if password == result:
                print('successful sign-in')
        except:
            print("unsuccessful login")
        finally:
            if not connection.closed:
                cursor.close()
                connection.close()
    return render_template('signin.html')


@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    '''
    Will be using a template. Likely will not need any input
    will need an output from the template in order to add the new user to the database
    '''
    if request.method == 'POST':
        user_name = request.form.get('userName', 'default value name')
        email = request.form.get('email', 'default value email')
        password = request.form.get('password', 'default value password')
        print('user name: ' + user_name)
        print('email: ' + email)
        print('password: ' + password)
        engine.execute("INSERT INTO user (user_name, user_email, user_phone_number, user_address, user_password) "
        "VALUES (?, ?, '(123)-456-7890', '123 ABC Street', ?);", ((user_name), (email), (password)))
    return render_template('signup.html')  # add user function
    # return 'sign up page'



@app.route('/buy_sell')
def buy_sell():
    '''
    Display buy or sell page
    '''
    return 'buy or sell page'


@app.route('/buy')
def list_of_items():
    '''
    use render template to load the data into whatever the template is
    This is the list of items page where each item is on display
    '''
    results = session.execute(text('select * from item'))
    data = []
    for r in results:
        data.append(dict(r))
    return jsonify(data)


@app.route('/item/<int:id>')
def get_item(id: int):
    results = session.execute(text('select * from item where item_id={}'.format(id)))
    data = []
    for r in results:
        data.append(dict(r))
    return jsonify(data)


@app.route('/sell', methods=['POST', 'GET'])
def sell_item():
    '''
    Will be using a template. Likely will not need any input
    will need an output from the template in order to add the new item to the database
    
    if request.method == 'POST':
        user = request.form
        return 'adding item please wait a moment'''  # add user function
    return 'add item page'


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
