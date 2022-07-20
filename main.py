from pprint import pprint
import requests
import googlemaps
import os
# import pandas as pd
import sqlalchemy as db
from flask import Flask, flash, redirect, jsonify, request, render_template, url_for
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
UPLOAD_FOLDER = 'week4-project/static/images'
app.config['SECRET_KEY'] = 'fec93d1b1cb7926beb25960608b25818'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

session = Session(engine)
user_data = None


'''@app.route('/<table_name>/<int:id>')
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
    return jsonify(data)'''


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def login():
    flash('hello')
    global user_data
    print(user_data)
    if request.method == 'POST':
        email = request.form.get('email', 'default value email')
        password = request.form.get('password', 'default value password')
        print('email: ' + email)
        print('password: ' + password)
        try:
            print('in try')
            user_results = session.execute(text("select * from user where user_email='{}'".format(str(email))))
            print(user_results)
            for r in user_results:
                print(r)
                user_data = dict(r)
            print(user_data)
            if password == user_data['user_password']:
                print("successful login")
                flash(f'Account created for you!', 'success')
                print(url_for('buy_sell'))
                return redirect('https://lucassaturn-preciseaugust-5000.codio.io/buy_sell')
            flash("unsuccessful login")
        except Exception as ex:
            print("unsuccessful login")
            print("error" + str(ex))
    return render_template('signin.html')

# for testing
@app.route('/user')
def get_table_data():
    results = session.execute(text('select * from user'))
    data = []
    for r in results:
        data.append(dict(r))
    return jsonify(data)

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
        phone_number = request.form.get('phoneNumber', 'default phone_number')
        address = request.form.get('address', 'default address')
        print('user name: ' + user_name)
        print('email: ' + email)
        print('password: ' + password)
        print('phone number: ' + phone_number)
        print('address: ' + address)
        engine.execute("INSERT INTO user (user_name, user_email, user_phone_number, user_address, user_password) "
        "VALUES (?, ?, ?, ?, ?);", (user_name, email, phone_number, address, password))
        return redirect('https://lucassaturn-preciseaugust-5000.codio.io/buy_sell')
        #return render_template('signin.html')
    return render_template('signup.html')  # add user function
    # return 'sign up page'



@app.route('/buy_sell', methods=['GET', 'POST'])
def buy_sell():
    '''
    Display buy or sell page
    '''
    print('HELLO')
    return render_template('buy_or_sell_page.html')


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
    return render_template('list_of_items_page.html', item_list=data)


@app.route('/item/<int:id>')
def get_item(id: int):
    item_results = session.execute(text('select * from item where item_id={}'.format(id)))
    item_data = {}
    for r in item_results:
        item_data = dict(r)
    seller_results = session.execute(text('select * from user where user_id={}'.format(item_data['seller_id'])))
    seller_data = {}
    for r in seller_results:
        seller_data = dict(r)
    location = map_client.distance_matrix(user_data['user_address'], seller_data['user_address'])
    distance_in_km = location['rows'][0]['elements'][0]['distance']['text']
    time = location['rows'][0]['elements'][0]['duration']['text']
    return render_template('itempage.html', item=item_data, seller=seller_data, distance=distance_in_km)


@app.route('/sell', methods=['POST', 'GET'])
def sell_item():
    global user_data
    print(user_data)
    '''
    Will be using a template. Likely will not need any input
    will need an output from the template in order to add the new item to the database
    
    if request.method == 'POST':
        user = request.form
        return 'adding item please wait a moment'''
    if request.method == 'POST':
        item_name = request.form.get('name', 'default item name')
        price = request.form.get('price', 'default price')
        description = request.form.get('itemDesc', 'default description')
        #img = request.files['photo']
        #phone_number = request.form.get('phoneNumber', 'default')
        print('item name: ' + item_name)
        print('price: ' + price)
        print('description: ' + description)
        # print('image path:' + img)
        
        #print('phone number: ' + phone_number)
        #print("form: " + str(request.form))
        id_num = 0
        try:
            connection = engine.connect()
            cursor = connection.execute("SELECT count(*) from item;")
            result = cursor.scalar()
            id_num = int(result) + 1
        except:
            print("something went wrong")
        finally:
            if not connection.closed:
                cursor.close()
                connection.close()
        engine.execute("INSERT INTO item (item_name, item_price, item_description, seller_id) "
        "VALUES (?, ?, ?, ?);", (item_name, price, description, user_data['user_id']))
        
        #path = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
        photo = request.files['photo']
        filename = '{}.png'.format(id_num)
        #path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
        #photo.save(path)  # add user function
        #filename = photo.filename
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('post_item.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
