from pprint import pprint
import requests
import googlemaps
import os
import pandas as pd
import sqlalchemy as db
from flask import Flask, jsonify, request
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


@app.route('/')
def hello():
    return 'hello world'


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


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")