# Modified by William @ 2021-03-19
from flask import Flask, request, Response, send_from_directory, jsonify
import os
import json
import sqlite3
from datetime import date

from . import routes

# 很怪，DB只能絕對路徑
DATABASE = os.path.join(
    os.path.dirname(__file__).replace(os.path.dirname(__file__), '', 1),
    'data\production_database.db'
)

tableName = 'work_item_process_method'

# Method : POST /processMethods/create
# Input : na
# Description : 新增 processMethod
@routes.route('/processMethods/create',  methods=['POST'])
def create():
    method_name = request.form['method_name']
    method_description = request.form['method_description']

    # empty check
    if not method_name:
        return jsonify({'state': 'error', 'msg': 'input method_name is empty'})

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # check exist
    sql = f'SELECT * FROM {tableName} WHERE method_name = "{method_name}"'
    print(sql)
    cursor.execute(sql)
    targets = cursor.fetchall()
    if len(targets) > 0:
        print('close')
        conn.close()
        return jsonify({'state': 'error', 'msg': 'method_name already exist'})
    
    sql = f'''
        INSERT INTO {tableName} (method_name, method_description)
        VALUES ("{method_name}", "{method_description}")
    '''
    print(sql)
    cursor.execute(sql)
    conn.commit()
    conn.close()

    return jsonify({'state':'success'})


# Method : POST /processMethods/update/id
# Input : na
# Description : 更新 processMethod by id
@routes.route('/processMethods/update/<int:id>',  methods=['POST'])
def update(id):
    method_name = request.form['method_name']
    method_description = request.form['method_description']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    sql = f'''
        UPDATE {tableName}
        SET method_name = "{method_name}", method_description = "{method_description}"
        WHERE method_id = { id }
    '''
    print(sql)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    return jsonify({'state': 'success'})


# Method : GET /processMethods
# Input : na
# Description : 取得全部加工方法
@routes.route('/processMethods')
def getAll():
    print('=======all=========')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    result = {}
    result["results"] = []
    sql = f'SELECT * FROM {tableName}'
    print(sql)
    cursor.execute(sql)
    tables = cursor.fetchall()

    for record in tables:
        r = {}
        n = 0
        for col in record:
            key = cursor.description[n][0]
            r[key] = col
            n += 1
        result["results"].append(r)
    return jsonify(result)


# Method : GET /processMethods/id
# Input : na
# Description : 取得單一加工方法詳細資料
@routes.route('/processMethods/<int:id>')
def getOne(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    result = {}
    result["results"] = []
    sql = f'SELECT * FROM {tableName} WHERE method_id = {id}'
    print(sql)
    cursor.execute(sql)
    tables = cursor.fetchall()
    for record in tables:
        r = {}
        n = 0
        for col in record:
            key = cursor.description[n][0]
            r[key] = col
            n += 1
        result["results"].append(r)
    return jsonify(result)


# Method : GET /processMethods/delete/id
# Input : na
# Description : 刪除加工方法詳細資料
@routes.route('/processMethods/delete/<int:id>')
def deleteOne(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    sql = f'DELETE FROM {tableName} WHERE method_id = {id}'
    print(sql)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    result = {'state': 'success'}
    return jsonify(result)
