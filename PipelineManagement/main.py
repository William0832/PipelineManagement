import os
from flask import Flask, request
import datetime



import json
import requests, csv, codecs, json
import os.path # for web routing to statistic files
from flask import Response, send_from_directory, jsonify
# from flask import Flask ,request
from flask import g
import importlib
import sqlite3
from datetime import date
from shutil import copyfile





DATABASE = 'data/production_database.db'

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
def root_dir():
  return os.path.abspath(os.path.dirname(__file__))



def getfile(filename):
  try:
    src = os.path.join(root_dir(), filename)
    return open(src).read()
  except IOError as exc:
    return str(exc)

@app.route('/<path:path>')
def send_web(path):
  return send_from_directory('web',path)

# Method : GET /pages/Dashboard_Customer/id
# Input : na
# Description : 取得客戶資料頁面
@app.route('/pages/Dashboard_Customer/<int:id>')
def getCustomerEditPage(id):
  return send_from_directory('web', 'pages/Record_Customer.html')

# Method : GET /customers
# Input : na
# Description : 取得所有客戶資料清
@app.route('/customers')
def getCustomers():
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  result = {}
  result["results"] = []
  search_sql = "SELECT * FROM customer ORDER BY customer_id"

  print(search_sql)
  cursor.execute(search_sql)
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

# Method : GET /customers/id
# Input : id
# Description : 取得所有客戶資料清
@app.route('/customers/<int:id>')
def getCustomer(id):
  print('get customer id',id)
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  result = {}
  result["results"] = []
  sql = f'Select * From customer Where customer_id = {id}'
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

# Method: POST / customer
# Input: na
# Description: 建立客戶資料
@app.route('/addCustomer', methods=['POST'])
def addCustomer():
  # create_dt = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
  form =  request.form
  colsStr = ''
  cols = []
  for k in form:
    colsStr += f'{k}, '
    cols.append(form[k])
    v = form[k]
  colsStr = colsStr[:-2]
  questions  = ('?,'*len(cols))[:-1]
  sql = f'INSERT INTO customer({colsStr}) VALUES ({questions})'
  print(sql)
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  cursor.execute(sql, cols)
  conn.commit()

  result = {}
  result["result"] = "success"
  result["message"] = "成功建立客戶資料" 
  return jsonify(result)

# Method: POST / customer/id
# Input: id
# Description: 更新客戶資料
@app.route('/updateCustomer/<int:id>', methods=['POST'])
def updateCustomer(id):
  print('update customer id', id)
  form = request.form

  tempSql = ''
  for k in form:
    tempSql += f'{k} = "{form[k]}",'
  tempSql = tempSql[:-1]
  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  sql = f'UPDATE customer SET {tempSql} WHERE customer_id = {id}'
  print(sql)
  cursor.execute(sql)
  conn.commit()

  result = {}
  result["result"] = "success"
  result["message"] = "成功更新客戶資料" 
  return jsonify(result)



# Method : POST /addWorkitem
# # Input : na
# # Decription : 建立工單，並建立治具與測試待處理項目

@app.route('/addWorkitem', methods=['POST'])
def addWorkitem():

  create_dt = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
  # uid = request.args.get('uid')
  customer_id = request.form['customer_id']
  part_no = request.form['part_no']
  lot_no = request.form['lot_no']
  creator = request.form['creator']
  test_style = request.form['test_style']
  
  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()

  cursor.execute('insert into record_work_item(customer_id, part_no,lot_no,creator,create_dt,test_style) values (?, ?,?,?,?,?)', [customer_id, part_no,lot_no,creator,create_dt,test_style])
  conn.commit()

  cursor.execute("select * from record_work_item order by create_dt desc limit 1")
  tables = cursor.fetchall()
  
  work_item_id = tables[0][0]

  prepare_type = "工程"
  prepare_tool = "待處理"


  cursor.execute('insert into record_prepare(type, tool,work_item_id,start_dt) values (?, ?,?,?)', [prepare_type, prepare_tool,work_item_id,create_dt])
  conn.commit()


  cursor.execute('insert into record_test(work_item_id,create_dt) values (?,?)', [work_item_id,create_dt])
  conn.commit()

  result = {}
  result["result"] = "success"
  result["message"] = "成功建立工單" 
  return jsonify(result)
  
  

# Method : GET /prepare/getWaitingItems 
# Input : na
# Decription : 取得待處理項目
@app.route('/prepare/getPrepareWaitings')
def getPrepareWaitingItems():

  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  # get roles
  result = {}
  result["results"] = []
  search_sql = "select i.tool_type,i.tool_id, i.tool_name, i.owner,  p.* from "
  search_sql += "(select * from tool_info  where  prepare_or_test = 'prepare' and tool_id = '待處理' )  i "
  search_sql += "left join "
  search_sql += "(select rp.* ,wi.* from record_prepare rp join record_work_item wi where rp.work_item_id = wi.work_item_id and rp.status = 'open') p "
  search_sql += "on i.tool_type = p.type and i.tool_id = p.tool "
    
  # print(search_sql)
  cursor.execute(search_sql)
  tables = cursor.fetchall()
    
  for record in tables:
    r = {}
    r["tool_type"]        = record[0]
    r["tool_id"]          = record[1]
    r["tool_name"]        = record[2]
    r["owner"]            = record[3]
    r["record_id"]        = record[4]
    r["status"]           = record[7]
    r["work_item_id"]     = record[8]
    r["start_dt"]         = record[9]
    r["customer_id"]      = record[13]
    r["part_no"]          = record[14]
    r["lot_no"]           = record[15]
    

    result["results"].append(r)




  return jsonify(result)  

# Method : GET /prepare/getPrepareToolStatus 
# Input : na
# Decription : 取得待處理項目
@app.route('/prepare/getPrepareToolStatus')
def getPrepareToolStatus():

  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  # get roles
  result = {}
  result["results"] = []
  search_sql = "select i.tool_type,i.tool_id, i.tool_name, i.owner,  p.* from "
  search_sql += "(select * from tool_info  where  prepare_or_test = 'prepare' and tool_id <> '待處理' )  i "
  search_sql += "left join "
  search_sql += "(select rp.* ,wi.* from record_prepare rp join record_work_item wi where rp.work_item_id = wi.work_item_id and rp.status='open') p "
  search_sql += "on i.tool_type = p.type and i.tool_id = p.tool "
    
  cursor.execute(search_sql)
  tables = cursor.fetchall()
    
  for record in tables:
    r = {}
    r["tool_type"]        = record[0]
    r["tool_id"]          = record[1]
    r["tool_name"]        = record[2]
    r["owner"]            = record[3]
    r["record_id"]        = record[4]
    r["status"]           = record[7]
    r["work_item_id"]     = record[8]
    r["start_dt"]         = record[9]
    r["customer_id"]      = record[13]
    r["part_no"]          = record[14]
    r["lot_no"]           = record[15]
    

    result["results"].append(r)




  return jsonify(result)  


# Method : GET /prepare/getPrepareDone 
# Input : na
# Decription : 取得待處理項目
@app.route('/prepare/getPrepareDone')
def getPrepareToolDone():

  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  # get roles
  result = {}
  result["results"] = []
  search_sql = "select i.tool_type,i.tool_id, i.tool_name, i.owner,  p.* from "
  search_sql += "(select * from tool_info  where  prepare_or_test = 'prepare' and tool_type = '完成'  and tool_id = '待處理' )  i "
  search_sql += "left join "
  search_sql += "(select rp.* ,wi.* from record_prepare rp join record_work_item wi where rp.work_item_id = wi.work_item_id and rp.status='open') p "
  search_sql += "on i.tool_type = p.type and i.tool_id = p.tool "
  print(search_sql)
  cursor.execute(search_sql)
  tables = cursor.fetchall()
    
  for record in tables:
    r = {}
    r["tool_type"]        = record[0]
    r["tool_id"]          = record[1]
    r["tool_name"]        = record[2]
    r["owner"]            = record[3]
    r["record_id"]        = record[4]
    r["status"]           = record[7]
    r["work_item_id"]     = record[8]
    r["start_dt"]         = record[9]
    r["customer_id"]      = record[13]
    r["part_no"]          = record[14]
    r["lot_no"]           = record[15]

    r["prepare_start_dt"] = record[33]
    r["prepare_end_dt"] = record[34]
    

    result["results"].append(r)




  return jsonify(result)  
  
# Method : POST /prepare/changePrepareRecordPhase
# # Input : na
# # Decription : 更新治具準備製程

@app.route('/prepare/changePrepareRecordPhase', methods=['POST'])
def changePrepareRecordPhase():

  
  create_dt = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
  end_dt = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
  # uid = request.args.get('uid')
  record_id = request.form['record_id']
  print("record_id = " + record_id)

  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()

  cursor.execute("select * from record_prepare where record_id = "+record_id )
  tables = cursor.fetchall()
  
  # record_id = tables[0][0]
  current_type = tables[0][1]
  current_tool = tables[0][2]
  current_status = tables[0][3]
  work_item_id = tables[0][4]
  start_dt = tables[0][5]
  # end_dt = tables[0][6]

  next_type = ""
  next_tool = "待處理"

  if current_type == "工程":
    next_type = "鑽孔"
  elif current_type == "鑽孔":
    next_type = "組裝"
  elif current_type == "組裝":
    next_type = "完成"
  
  cursor.execute('update record_prepare set status = "closed" , end_dt = "'+end_dt+'"  where record_id = '+record_id)
  conn.commit()

  cursor.execute('insert into record_prepare(type, tool,work_item_id,start_dt) values (?, ?,?,?)', [next_type, next_tool,work_item_id,create_dt])
  conn.commit()

  
  if next_type == "完成":
    cursor.execute('update record_work_item set prepare_end_dt = "'+end_dt+'" where work_item_id = '+work_item_id)
    conn.commit()


  result = {}
  result["result"] = "success"
  result["message"] = "成功更新治具製程狀態" 
  return jsonify(result)

    
# Method : POST /prepare/finishPrepareRecordPhase
# # Input : na
# # Decription : 完成治具準備製程

@app.route('/prepare/finishPrepareRecordPhase', methods=['POST'])
def finishPrepareRecordPhase():

  
  create_dt = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
  end_dt = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
  # uid = request.args.get('uid')
  record_id = request.form['record_id']
  print("record_id = " + record_id)

  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()

  cursor.execute("select * from record_prepare where record_id = "+record_id )
  tables = cursor.fetchall()
  
  # record_id = tables[0][0]
  current_type = tables[0][1]
  current_tool = tables[0][2]
  current_status = tables[0][3]
  work_item_id = tables[0][4]
  start_dt = tables[0][5]
  # end_dt = tables[0][6]

  next_type = ""
  next_tool = "待處理"

  if current_type == "工程":
    next_type = "鑽孔"
  elif current_type == "鑽孔":
    next_type = "組裝"
  elif current_type == "組裝":
    next_type = "完成"
  
  cursor.execute('update record_prepare set status = "closed" , end_dt = "'+end_dt+'"  where record_id = '+record_id)
  conn.commit()

  cursor.execute('insert into record_prepare(type, tool,work_item_id,start_dt) values (?, ?,?,?)', [next_type, next_tool,work_item_id,create_dt])
  conn.commit()


  if next_type == "完成":
    cursor.execute('update record_work_item set prepare_end_dt = "'+end_dt+'", status="待處理" where work_item_id = '+work_item_id)
    conn.commit()


  result = {}
  result["result"] = "success"
  result["message"] = "成功更新治具製程狀態" 
  return jsonify(result)  
# Method : POST /prepare/changePrepareRecordPhase
# # Input : na
# # Decription : 更新治具準備製程

@app.route('/prepare/checkInPrepareRecord', methods=['POST'])
def checkInPrepareRecord():

  
  create_dt = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
  end_dt = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
  # uid = request.args.get('uid')
  record_id = request.form['record_id']
  select_tool_id = request.form['select_tool_id']

  print("record_id = " + record_id)

  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()

  cursor.execute("select * from record_prepare where record_id = "+record_id )
  tables = cursor.fetchall()
  
  # record_id = tables[0][0]
  current_type = tables[0][1]
  current_tool = tables[0][2]
  current_status = tables[0][3]
  work_item_id = tables[0][4]
  start_dt = tables[0][5]
  # end_dt = tables[0][6]


  
  
  cursor.execute('update record_prepare set status = "closed" , end_dt = "'+end_dt+'"  where record_id = '+record_id)
  conn.commit()

  cursor.execute('insert into record_prepare(type, tool,work_item_id,start_dt) values (?, ?,?,?)', [current_type, select_tool_id,work_item_id,create_dt])
  conn.commit()


  if current_type == "工程":
    cursor.execute('update record_work_item set prepare_start_dt = "'+create_dt+'"  where work_item_id = '+work_item_id)
    conn.commit()


  result = {}
  result["result"] = "success"
  result["message"] = "成功更新治具製程狀態" 
  return jsonify(result)



# Method : GET /prepare/getWaitingItems 
# Input : na
# Decription : 取得待處理項目
@app.route('/testing/getTestWaitings')
def getTestWaitings():

  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  # get roles
  result = {}
  result["results"] = []
  search_sql = "select rt.* ,wi.* from record_test rt, record_work_item wi "
  search_sql += "where rt.work_item_id = wi.work_item_id and rt.status = 'open'  and rt.test_tool_id is null"
    
  print(search_sql)
  cursor.execute(search_sql)
  tables = cursor.fetchall()
    
  for record in tables:
    r = {}
    r["tool_type"]        = record[2]
    r["tool_id"]          = record[3]
    # r["tool_name"]        = record[2]
    # r["owner"]            = record[3]
    r["test_record_id"]        = record[0]
    r["work_item_id"]     = record[1]

    r["start_dt"]         = record[29]
    r["customer_id"]      = record[33]
    r["part_no"]          = record[34]
    r["lot_no"]           = record[35]


    r["work_item_status"]           = record[59]


    result["results"].append(r)




  return jsonify(result)  


# Method : GET /testing/getTools 
# Input : na
# Decription : 取得生產測試機台
@app.route('/testing/getTools/<string:prepare_or_test>')
def getTools(prepare_or_test):

  print("getTools")
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  # get roles
  result = {}
  result["results"] = []
  
  search_sql = "select * from tool_info where prepare_or_test = '"+prepare_or_test+"' and tool_id <> '待處理'"

  if prepare_or_test == 'all':
    search_sql = "select * from tool_info where  tool_id <> '待處理'"  

  print(search_sql)
  cursor.execute(search_sql)
  tables = cursor.fetchall()
    
  for record in tables:
    r = {}
    r["tool_type"]        = record[1]
    r["tool_id"]          = record[2]
    r["tool_name"]        = record[3]
    r["owner"]            = record[4]


    result["results"].append(r)




  return jsonify(result)  


# Method : GET /testing/getTestToolStatus
# Input : na
# Decription : 取得待處理項目
@app.route('/testing/getTestToolStatus')
def getTestToolStatus():

  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  # get roles
  result = {}
  result["results"] = []
  search_sql = "select i.tool_type,i.tool_id, i.tool_name, i.owner,  p.* from "
  search_sql += "(select * from tool_info  where  prepare_or_test = 'test' and tool_id <> '待處理' )  i "
  search_sql += "left join "
  search_sql += "(select rt.* ,wi.* from record_test rt join record_work_item wi where rt.work_item_id = wi.work_item_id and rt.status = 'open') p "
  search_sql += "on i.tool_type = p.test_tool_type and i.tool_id = p.test_tool_id"
    
  print("getTestToolStatus :  "+ search_sql)
  cursor.execute(search_sql)
  tables = cursor.fetchall()
    
  for record in tables:
    r = {}
    r["tool_type"]        = record[0]
    r["tool_id"]          = record[1]
    r["tool_name"]        = record[2]
    r["owner"]            = record[3]
    r["record_id"]        = record[4]
    r["work_item_id"]     = record[5]
    r["start_dt"]         = record[36]
    r["customer_id"]      = record[37]
    r["part_no"]          = record[38]
    r["lot_no"]           = record[39]

    

    result["results"].append(r)




  return jsonify(result)  
    
# Method : POST /prepare/checkInTestRecord
# # Input : na
# # Decription : 更新測試機台

@app.route('/testing/checkInTestRecord', methods=['POST'])
def checkInTestRecord():

  
  start_dt = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
  end_dt = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
  # uid = request.args.get('uid')
  record_id = request.form['record_id']
  select_tool_id = request.form['select_tool_id']

  print("record_id = " + record_id)

  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()

  cursor.execute("select * from record_test where test_record_id = "+record_id )
  tables = cursor.fetchall()
  
  work_item_id = tables[0][1]


  
  
  cursor.execute('update record_test set test_tool_id = "'+select_tool_id+'" , test_start_dt = "'+start_dt+'"  where test_record_id = '+record_id)
  conn.commit()


  cursor.execute('update record_work_item set  test_start_dt = "'+start_dt+'", status = "測試中" where work_item_id = '+work_item_id)
  conn.commit()

  # cursor.execute('insert into record_prepare(type, tool,work_item_id,start_dt) values (?, ?,?,?)', [current_type, select_tool_id,work_item_id,create_dt])
  # conn.commit()



  result = {}
  result["result"] = "success"
  result["message"] = "成功指定生產機台" 
  return jsonify(result)

      
# Method : POST /prepare/checkInFlyTestRecord
# # Input : na
# # Decription : 更新測試機台

@app.route('/testing/checkInFlyTestRecord', methods=['POST'])
def checkInFlyTestRecord():

  
  start_dt = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
  end_dt = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
  # uid = request.args.get('uid')
  record_id = request.form['record_id']
  select_tool_id = request.form['select_tool_id']

  print("record_id = " + record_id)
  print("select_tool_id = " + select_tool_id)

  select_tools = select_tool_id[:-1].split(',')
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()

  cursor.execute("select * from record_test where test_record_id = "+record_id )
  tables = cursor.fetchall()
  
  work_item_id = tables[0][1]
  test_tool_type = tables[0][2]
  create_dt = tables[0][29]

  tool_count = 0

  for tool_id in select_tools:
    tool_count+=1
    if tool_count > 1:
      
      cursor.execute('insert into record_test(work_item_id,test_tool_type,test_tool_id,create_dt) values (?,?,?,?)', [work_item_id,test_tool_type,tool_id,create_dt])
      conn.commit()
    else:
      cursor.execute('update record_test set test_tool_id = "'+tool_id+'" , test_start_dt = "'+start_dt+'"  where test_record_id = '+record_id)
      conn.commit()
    
    

    
  
  
  


  cursor.execute('update record_work_item set  test_start_dt = "'+start_dt+'", status = "測試中" where work_item_id = '+work_item_id)
  conn.commit()

  # cursor.execute('insert into record_prepare(type, tool,work_item_id,start_dt) values (?, ?,?,?)', [current_type, select_tool_id,work_item_id,create_dt])
  # conn.commit()



  result = {}
  result["result"] = "success"
  result["message"] = "成功指定生產機台" 
  return jsonify(result)

# Method : POST /prepare/finishTestRecord
# # Input : na
# # Decription : 完成測試機台

@app.route('/testing/finishTestRecord', methods=['POST'])
def finishTestRecord():

  
  start_dt = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
  end_dt = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
  # uid = request.args.get('uid')
  record_id = request.form['record_id']
  select_tool_id = request.form['select_tool_id']

  print("record_id = " + record_id)

  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()

  cursor.execute("select * from record_test where test_record_id = "+record_id )
  tables = cursor.fetchall()
  
  work_item_id = tables[0][1]


  
  
  cursor.execute('update record_test set test_end_dt = "'+end_dt+'"  where test_record_id = '+record_id)
  conn.commit()


  cursor.execute('update record_work_item set  test_end_dt = "'+end_dt+'", status = "測試完成待包裝ㄔ" where work_item_id = '+work_item_id)
  conn.commit()

  # cursor.execute('insert into record_prepare(type, tool,work_item_id,start_dt) values (?, ?,?,?)', [current_type, select_tool_id,work_item_id,create_dt])
  # conn.commit()



  result = {}
  result["result"] = "success"
  result["message"] = "成功指定生產機台" 
  return jsonify(result)


# Method : GET /workitem/getWorkitems 
# Input : na
# Decription : 取得待處理項目
@app.route('/workitem/getWorkitems')
def getWorkitems():

  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  # get roles
  result = {}
  result["results"] = []
  search_sql = "select * from record_work_item order by work_item_id desc"
    
  print(search_sql)
  cursor.execute(search_sql)
  tables = cursor.fetchall()
    
  for record in tables:
    r = {}
    r["test_type"]        = record[5]
    r["create_dt"]          = record[1]
    r["test_style"]        = record[6]
    r["customer_id"]            = record[2]
    r["part_no"]        = record[3]
    r["lot_no"]     = record[4]

    r["units"]         = record[29]
    r["process"]      = record[30]
    r["status"]          = record[28]
    r["work_item_id"]           = record[0]


    result["results"].append(r)




  return jsonify(result)  

#  ---------



# Method : GET /pat/getCustomerInfo/<string:customer_name>  
# Input : na
# Decription : get pat customer info
@app.route('/product/getProductionReport')
def getProductionReport():

  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  

  # get report
  search_sql = "select * from record_test"
    
  cursor.execute(search_sql)
  tables = cursor.fetchall()
    
  result = {}
  result["results"] = []

  for record in tables:
    r = {}
   
    r["shift"]  = record[5]
    r["productionDate"]  = record[6]
    r["customer"]  = record[7]
    r["part_no"]  = record[8]
    r["program_name"]  = record[9]
    r["param_v"]  = record[10]
    r["param_phm"]  = record[11]
    r["param_mohm"]  = record[12]
    r["test_point_count"]  = record[13]
    r["work_item_count"]  = record[14]
    r["retest_rate"]  = record[15]
    r["batch_number"]  = record[16]
    r["first_piece_pintrack"]  = record[17]
    r["test_200"]  = record[18]
    r["testing_count"]  = record[19]
    r["test_result_ok_count"]  = record[20]
    r["test_result_ng_count"]  = record[21]
    r["yield"]  = record[22]
    r["defect"]  = record[23]
    r["test_start_time"]  = record[24]
    r["test_end_time"]  = record[25]
    r["abnormal_event"]  = record[26]
    r["event_start_time"]  = record[27]
    r["event_end_time"]  = record[28]
    r["tester"]  = record[29]
    r["test_machine"]  = record[30]

    result["results"].append(r)




  return jsonify(result)




# Method : GET /pat/getCustomerInfo/<string:customer_name>  
# Input : na
# Decription : get pat customer info
@app.route('/role/getRoles')
def getRoles():

  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  # get roles
  result = {}
  result["results"] = []
  search_sql = "select r.* from script_role r"
    
  cursor.execute(search_sql)
  tables = cursor.fetchall()
    
  for record in tables:
    r = {}
    r["script_id"]  = record[0]
    r["role_id"]         = str(record[1])
    r["role_name"]         = record[2]
    r["role_alias"]         = record[3]
    r["role_description"]         = record[4]
    r["role_photo_link"]         = record[5]
    

    result["results"].append(r)




  return jsonify(result)







# Method : GET /getCustomerInfo/<string:customer_name>  
# Input : na
# Decription : get customer info
@app.route('/getCustomerList/<string:tam_alias>')
def getCustomerList(tam_alias):

  print("Access Customer List Page, user: " + request.remote_user)
  permission = checkUserPermission(request.remote_user)

  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  # cursor.execute("select c.*, s.* from customer_survey_overall s, customer_info c  where tam_1 like '"+tam_alias+"' and c.customer_name = s.customer_name")
  # tables = cursor.fetchall()
  print("get customer list ")

  search_sql = ""
  if tam_alias == "null":
    
    if permission == "guest":
      tam_alias = "Demo"
      search_sql = "select a.*, w.cnt, e.sentiment from (select c.*, s.* from tam_info t, customer_survey_overall s, customer_info c  where ((t.esm_top like '"+tam_alias+"' or t.esm like '"+tam_alias+"' )  or c.tam_1 like '"+tam_alias+"') and t.tam_alias = c.tam_1 and c.customer_name = s.customer_name) a LEFT JOIN (select customer_name, count(workload_id) as cnt from customer_workload group by customer_name ) w  on  a.customer_name = w.customer_name LEFT JOIN customer_experience e  on  w.customer_name = e.customer_name and e.latest like 'Y'"

    elif permission == "pilot":
      print("default + pilot")
      tam_alias = request.remote_user
      # search_sql = "select a.*, w.cnt from (select c.*, s.* from customer_survey_overall s, customer_info c  where c.poc like 'chi_pilot' and c.customer_name = s.customer_name) a LEFT JOIN (select customer_name, count(workload_id) as cnt from customer_workload group by customer_name ) w  on  a.customer_name = w.customer_name"
      search_sql = "select a.*, w.cnt, e.sentiment from (select c.*, s.* from tam_info t, customer_survey_overall s, customer_info c  where ((t.esm_top like '"+tam_alias+"' or t.esm like '"+tam_alias+"' )  or c.tam_1 like '"+tam_alias+"'  or c.tam_1 like 'TAM_Alias') and t.tam_alias = c.tam_1 and c.customer_name = s.customer_name) a LEFT JOIN (select customer_name, count(workload_id) as cnt from customer_workload group by customer_name ) w  on  a.customer_name = w.customer_name LEFT JOIN customer_experience e  on  w.customer_name = e.customer_name and e.latest like 'Y'"
      
    elif permission == "gcr":
      print("default + gcr")
      # tam_alias = "jeffaws"
      search_sql = "select a.*, w.cnt, e.sentiment from (select c.*, s.* from tam_info t, customer_survey_overall s, customer_info c  where ((t.esm_top like '"+tam_alias+"' or t.esm like '"+tam_alias+"' )  or c.tam_1 like '"+tam_alias+"'  or c.tam_1 like 'TAM_Alias') and t.tam_alias = c.tam_1 and c.customer_name = s.customer_name) a LEFT JOIN (select customer_name, count(workload_id) as cnt from customer_workload group by customer_name ) w  on  a.customer_name = w.customer_name LEFT JOIN customer_experience e  on  w.customer_name = e.customer_name and e.latest like 'Y'"

    elif permission == "admin":
      print("default + admin")
      search_sql = "select a.*, w.cnt, e.sentiment from (select c.*, s.* from tam_info t, customer_survey_overall s, customer_info c  where t.tam_alias = c.tam_1 and c.customer_name = s.customer_name) a LEFT JOIN (select customer_name, count(workload_id) as cnt from customer_workload group by customer_name ) w  on  a.customer_name = w.customer_name LEFT JOIN customer_experience e  on  w.customer_name = e.customer_name and e.latest like 'Y'"
      


  # elif tam_alias == "CHI Pilot":
  #   print("CHI Pilot")

  
  else:
    check_input = checkUserPermission(tam_alias)
    print("checkUserPermission(tam_alias): " + check_input)
    if permission == "admin":
      search_sql = "select a.*, w.cnt, e.sentiment from (select c.*, s.* from tam_info t, customer_survey_overall s, customer_info c  where ((t.esm_top like '"+tam_alias+"' or t.esm like '"+tam_alias+"' )  or c.tam_1 like '"+tam_alias+"') and t.tam_alias = c.tam_1 and c.customer_name = s.customer_name) a LEFT JOIN (select customer_name, count(workload_id) as cnt from customer_workload group by customer_name ) w  on  a.customer_name = w.customer_name LEFT JOIN customer_experience e  on  w.customer_name = e.customer_name and e.latest like 'Y'"
      print("admin : " + search_sql)


    elif check_input == permission:
      print(tam_alias + " + " + request.remote_user)
      search_sql = "select a.*, w.cnt, e.sentiment from (select c.*, s.* from tam_info t, customer_survey_overall s, customer_info c  where ((t.esm_top like '"+tam_alias+"' or t.esm like '"+tam_alias+"' )  or c.tam_1 like '"+tam_alias+"') and t.tam_alias = c.tam_1 and c.customer_name = s.customer_name) a LEFT JOIN (select customer_name, count(workload_id) as cnt from customer_workload group by customer_name ) w  on  a.customer_name = w.customer_name LEFT JOIN customer_experience e  on  w.customer_name = e.customer_name and e.latest like 'Y'"

    else:  
      print(tam_alias + " + " + request.remote_user)
      if tam_alias == "jeffaws" & permission =="gcr":
        tam_alias = "jeffaws"
        search_sql = "select a.*, w.cnt, e.sentiment from (select c.*, s.* from tam_info t, customer_survey_overall s, customer_info c  where ((t.esm_top like '"+tam_alias+"' or t.esm like '"+tam_alias+"' )  or c.tam_1 like '"+tam_alias+"') and t.tam_alias = c.tam_1 and c.customer_name = s.customer_name) a LEFT JOIN (select customer_name, count(workload_id) as cnt from customer_workload group by customer_name ) w  on  a.customer_name = w.customer_name LEFT JOIN customer_experience e  on  w.customer_name = e.customer_name and e.latest like 'Y'"
      else:
        tam_alias = ""
        search_sql = "select a.*, w.cnt, e.sentiment from (select c.*, s.* from tam_info t, customer_survey_overall s, customer_info c  where ((t.esm_top like '"+tam_alias+"' or t.esm like '"+tam_alias+"' )  or c.tam_1 like '"+tam_alias+"') and t.tam_alias = c.tam_1 and c.customer_name = s.customer_name) a LEFT JOIN (select customer_name, count(workload_id) as cnt from customer_workload group by customer_name ) w  on  a.customer_name = w.customer_name LEFT JOIN customer_experience e  on  w.customer_name = e.customer_name and e.latest like 'Y'"

    
  cursor.execute(search_sql)
  tables = cursor.fetchall()
    
  result = {}
  result["results"] = []

  for record in tables:
    r = {}
    r["customer"] = record[0]
    r["tam_1"] = record[1]
    r["tam_2"] = record[2]
    r["tam_3"] = record[3]
    r["tam_4"] = record[4]
    r["tam_5"] = record[5]
    r["customer_domain"] = record[6]
    r["summary"] = record[10]
    r["tam_alias"] = record[16]
    r["update_dt"] = record[17]
    r["complete_survey"] = record[18]
    r["complete_comment"] = record[19]
    r["q1"] = record[11]
    r["q2"] = record[12]
    r["q3"] = record[13]
    r["q4"] = record[14]
    r["q5"] = record[15]
    # r["sentiment"] = record[20]
    r["workload_count"] = record[21]
    r["cex"] = record[22]

    result["results"].append(r)




  return jsonify(result)




# Method : GET /pat/getCustomerInfo/<string:customer_name>  
# Input : na
# Decription : get pat customer info
@app.route('/pat/getCustomerList')
def getPATCustomerList():

  print("Access PAT Customer List Page, user: " + request.remote_user)
  permission = checkUserPermission(request.remote_user)

  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  # cursor.execute("select c.*, s.* from customer_survey_overall s, customer_info c  where tam_1 like '"+tam_alias+"' and c.customer_name = s.customer_name")
  # tables = cursor.fetchall()
  print("get pat customer list ")

  search_sql = "select p.*, c.tam_1, r.revenue from customer_pipeline_info p"
  search_sql += " left join customer_info c on p.customer_name = c.customer_name"
  search_sql += " left join customer_revenue r on p.customer_name = r.customer_name and r.latest= 'Y'"
  search_sql += " left join customer_status s on p.customer_name = s.customer_name and s.latest= 'Y'"


  # elif tam_alias == "CHI Pilot":
  #   print("CHI Pilot")

  
    
  cursor.execute(search_sql)
  tables = cursor.fetchall()
    
  result = {}
  result["results"] = []

  for record in tables:
    r = {}
    r["customer_name"] = record[0]
    r["region"] = record[2]
    r["esm"] = record[9]
    r["bd"] = record[4]
    r["support_plan"] = record[5]
    r["revenue"] = record[10]
    r["industry"] = record[6]
    r["cx_status"] = record[7]
    r["insights"] = record[8]

                
                


    result["results"].append(r)




  return jsonify(result)




# Method : GET /pat/getCustomerInfo/<string:customer_name>  
# Input : na
# Decription : get PAT CommunicationLog
@app.route('/pat/getCommunicationLog/<string:customer_name>')
def getCommunicationLog(customer_name):

  print("Access PAT Customer communication log, user: " + request.remote_user)
  permission = checkUserPermission(request.remote_user)

  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  # cursor.execute("select c.*, s.* from customer_survey_overall s, customer_info c  where tam_1 like '"+tam_alias+"' and c.customer_name = s.customer_name")
  # tables = cursor.fetchall()
  print("get pat customer list ")

  search_sql = "select * from communication_log where customer_name like '"+customer_name+"' order by seq desc"


    
  cursor.execute(search_sql)
  tables = cursor.fetchall()
    
  result = {}
  result["results"] = []

  for record in tables:
    r = {}
    r["customer_name"] = record[1]
    r["esm"] = record[2]
    r["date"] = record[3]
    r["activity"] = record[4]
    r["investiment_hrs"] = record[5]
    r["action_completed"] = record[6]
    r["next_action_plan"] = record[7]

                
                


    result["results"].append(r)




  return jsonify(result)



# Method : GET /getTAMList
# Input : na
# Decription : get tam list
@app.route('/getTAMList')
def getTAMList():

  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  # cursor.execute("select c.*, s.* from customer_survey_overall s, customer_info c  where tam_1 like '"+tam_alias+"' and c.customer_name = s.customer_name")
  # tables = cursor.fetchall()

  # if len(tables) == 0 :
  cursor.execute("select tam_alias from tam_info order by tam_alias")
  tables = cursor.fetchall()
  
  result = {}
  result["results"] = []

  for record in tables:
    r = {}
    r["tam_alias"] = record[0]
  
    result["results"].append(r)




  return jsonify(result)


# Method : GET /getCurrentUser
# Input : na
# Decription : get current user
@app.route('/getCurrentUser')
def getCurrentUser():
  user = request.remote_user

 
  result = {}
  result["user_alias"] = user


  return jsonify(result)

# Method :  /checkUserPermission
# Input : na
# Decription : check user permission
def checkUserPermission(user_alias):
  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  cursor.execute("select permission from acct_permission where acct_alias like '"+user_alias+"'")
  tables = cursor.fetchall()  

  if len(tables) == 0 :
    return "guest"
  else:
    return tables[0][0]
  




# Method : GET /getMemberList/<string:tam_alias>
# Input : na
# Decription : get tam list
@app.route('/getMemberList/<string:tam_alias>')
def getMemberList(tam_alias):

  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  permission = checkUserPermission(request.remote_user)

  result = {}
  result["results"] = []
  
  if tam_alias == "null":
    query_sql = ""
    if permission == "guest":
      print("default + guest")
      query_sql = "select distinct tam_alias from tam_info where esm like 'Demo' order by tam_alias"

    elif permission == "pilot":
      print("default + pilot")
      query_sql = "select distinct tam_alias from tam_info where esm like '"+request.remote_user+"' order by tam_alias"

    elif permission == "gcr":
      print("default + gcr")
      query_sql = "select distinct esm from tam_info where esm_top like 'jeffaws' order by tam_alias"

    elif permission == "admin":
      print("default + admin")
      query_sql = "select distinct tam_alias from tam_info order by tam_alias"
      print(query_sql)
    cursor.execute(query_sql)
    tables = cursor.fetchall()

    for record in tables:
      r = {}
      r["tam_alias"] = record[0]
      result["results"].append(r)

  elif tam_alias == "CHI Pilot":
    print("CHI Pilot")

  
  else:
    check_input = checkUserPermission(tam_alias)
    # if check_input == permission:
    #   print(tam_alias + " + " + request.remote_user)
      

    # else:  
    #   print(tam_alias + " + " + request.remote_user)
    cursor.execute("select distinct  esm from tam_info where esm_top like '"+tam_alias+"' order by esm")
    tables = cursor.fetchall()
    
    result = {}
    result["results"] = []

    if len(tables) > 0 :

      for record in tables:
        r = {}
        r["tam_alias"] = record[0]
      
        result["results"].append(r)
    else:
      cursor.execute("select distinct tam_alias from tam_info where esm like '"+tam_alias+"' order by tam_alias")
      tables = cursor.fetchall()
      result = {}
      result["results"] = []

      for record in tables:
        r = {}
        r["tam_alias"] = record[0]
      
        result["results"].append(r)

  # cursor.execute("select c.*, s.* from customer_survey_overall s, customer_info c  where tam_1 like '"+tam_alias+"' and c.customer_name = s.customer_name")
  # tables = cursor.fetchall()

  # if len(tables) == 0 :
  

    
  return jsonify(result)

# Method : GET /getTAMInfo
# Input : na
# Decription : get ESM by TAM
@app.route('/getTAMInfo/<string:tam_alias>')
def getTAMInfo(tam_alias):
  
  permission = checkUserPermission(request.remote_user)

  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()

  result = {}
  
  if tam_alias == "null":

    if permission == "guest":
      print("default + guest")
      result["gcr"] = "Demo"
      result["esm"] = "Demo"
      result["tam"] = "Demo"

    elif permission == "pilot":
      print("default + pilot")
      result["gcr"] = "CHI Pilot"
      result["esm"] = "CHI Pilot"
      result["tam"] = request.remote_user

    elif permission == "gcr":
      print("default + gcr")

      cursor.execute("select * from tam_info where tam_alias like '"+request.remote_user+"'")
      tables = cursor.fetchall()
      
      result["gcr"] = tables[0][0]
      result["esm"] = tables[0][1]
      result["tam"] = tables[0][2]

    elif permission == "admin":
      print("default + admin")

      result["gcr"] = ""
      result["esm"] = ""
      result["tam"] = ""

  elif tam_alias == "CHI Pilot":
    print("CHI Pilot")
    result["gcr"] = "CHI Pilot"
    result["esm"] = "CHI Pilot"
    result["tam"] = "CHI Pilot"

  
  else:

    check_input = checkUserPermission(tam_alias)

    if permission == "admin":
      print(tam_alias + " + " + request.remote_user)


      cursor.execute("select * from tam_info where tam_alias like '"+tam_alias+"'")
      print("select * from tam_info where tam_alias like '"+tam_alias+"'")
      tables = cursor.fetchall()
      

      result["gcr"] = tables[0][0]
      result["esm"] = tables[0][1]
      result["tam"] = tables[0][2]

    elif check_input == permission:
      print(tam_alias + " + " + request.remote_user)


      cursor.execute("select * from tam_info where tam_alias like '"+tam_alias+"'")
      print("select * from tam_info where tam_alias like '"+tam_alias+"'")
      tables = cursor.fetchall()
      

      result["gcr"] = tables[0][0]
      result["esm"] = tables[0][1]
      result["tam"] = tables[0][2]


    else:  
      print(tam_alias + " + " + request.remote_user)
      result["gcr"] = "Demo"
      result["esm"] = "Demo"
      result["tam"] = "Demo"
  


  return jsonify(result)

# Method : GET /getCustomerWorkload/<string:customer_name>  
# Input : na
# Decription : get customer info
@app.route('/getCustomerWorkload/<string:customer_name>')
def getCustomerWorkload(customer_name):

  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  # cursor.execute("select c.*, s.* from customer_survey_overall s, customer_info c  where tam_1 like '"+tam_alias+"' and c.customer_name = s.customer_name")
  # tables = cursor.fetchall()

  # if len(tables) == 0 :
  cursor.execute("select w.customer_name,w.workload_name,w.workload_id, a.a1_1,a.a1_2,a.a1_3,a.a1_4,a.update_dt,a.latest from customer_workload w LEFT JOIN (SELECT workload_id, a1_1, a1_2,a1_3,a1_4,update_dt,latest FROM workload_survey_answer WHERE LATEST LIKE 'Y') a ON w.workload_id = a.workload_id  where w.customer_name like '"+customer_name+"'")  




  tables = cursor.fetchall()
  
  result = {}
  result["workloads"] = []

  for record in tables:
    r = {}
    r["customer_name"] = record[0]
    r["workload_name"] = record[1]
    r["workload_id"] = record[2]
    r["a1_1"] = record[3]
    r["a1_2"] = record[4]
    r["a1_3"] = record[5]
    r["a1_4"] = record[6]
    r["update_dt"] = record[7]
  
    result["workloads"].append(r)




  return jsonify(result)



# Method : GET /getAcctList  
# Input : na
# Decription : get acct permission
@app.route('/getAcctList')
def getAcctList():

  permission = checkUserPermission(request.remote_user)

  if permission == "admin":
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # cursor.execute("select c.*, s.* from customer_survey_overall s, customer_info c  where tam_1 like '"+tam_alias+"' and c.customer_name = s.customer_name")
    # tables = cursor.fetchall()

    # if len(tables) == 0 :
    cursor.execute("select * from acct_permission")  




    tables = cursor.fetchall()

    result = {}
    result["result"] = "success"
    result["accts"] = []

    for record in tables:
      r = {}
      r["acct_alias"] = record[0]
      r["permission"] = record[1]

      result["accts"].append(r)

  else:

    result = {}
    result["result"] = "fail"
  



  return jsonify(result)


# Method : GET /getCustomerInfo/<string:customer_name>  
# Input : na
# Decription : get customer info
@app.route('/getCustomerInfo/<string:customer_name>')
def getCustomerInfo(customer_name):

  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  cursor.execute("select * from customer_info where customer_name like '"+customer_name+"'")
  tables = cursor.fetchall()
  
  result = {}
  result["tam_alias"] = tables[0][1]

  return jsonify(result)


# Method : GET /getCustomerSurveySummary/<string:customer_name>  
# Input : na
# Decription : get service list for testing, debug & verification 
@app.route('/getCustomerSurveySummary/<string:customer_name>')
def getCustomerSurveySummary(customer_name):

  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  cursor.execute("select * from customer_survey_overall where customer_name like '"+customer_name+"'")
  tables = cursor.fetchall()
  if len(tables) == 0 :
    cursor.execute('insert into customer_survey_overall(customer_name, summary) values (?, ?)', [customer_name,"please input TAM's summary for the customer"])
    conn.commit()
    cursor.execute("select * from customer_survey_overall where customer_name like '"+customer_name+"'")
    tables = cursor.fetchall()


  summary = tables[0][1]
  q1_score = tables[0][2]
  q2_score = tables[0][3]
  q3_score = tables[0][4]
  q4_score = tables[0][5]
  q5_score = tables[0][6]

  tamalias = tables[0][7]
  update_dt = tables[0][8]
  # sentiment_score = tables[0][11]

  if q1_score is None:
    q1_score = 0
  if q2_score is None:
    q2_score = 0

  if q3_score is None:
    q3_score = 0
  if q4_score is None:
    q4_score = 0

  if q5_score is None:
    q5_score = 0
  # if sentiment_score is None:
  #   sentiment_score = 0

  result = {}
  result["result"] = "success"
  result["summary"] = summary
  result["tamalias"] = tamalias
  result["update_dt"] = update_dt

  result["scores"] = []
  result["scores"].append({"catg":"Business Continuity by Workload","type":"5star","score":q1_score})
  result["scores"].append({"catg":"People Readiness","type":"5star","score":q2_score})
  result["scores"].append({"catg":"Cost Optimization","type":"5star","score":q3_score})
  result["scores"].append({"catg":"Technology Innovation","type":"5star","score":q4_score})
  result["scores"].append({"catg":"Security","type":"5star","score":q5_score})
  # result["scores"].append({"catg":"Customer Experience","type":"5star","score":sentiment_score})

  return jsonify(result)
# {
#     "scores":[
        
#     ]
# }



# Method : GET /getCustomerSurveyAnswer/<string:customer_name>  
# Input : na
# Decription : get customer info
@app.route('/getCustomerSurveyAnswer/<string:customer_name>')
def getCustomerSurveyAnswer(customer_name):

  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  
  cursor.execute("select * from (select * from customer_info where customer_name like '"+customer_name+"') i left join (select * from customer_survey_answer where latest='Y') a on i.customer_name=a.customer_name ")
  tables = cursor.fetchall()
  
  result = {}
  result["customer_name"] = tables[0][0]
  result["tam_1"] = tables[0][1]
  result["customer_domain"] = tables[0][6]
  result["es_type"] = tables[0][7]
  result["tam_alias"] = tables[0][10]
  result["a2_1"] = tables[0][11]
  result["a2_2"] = tables[0][12]
  result["a3_1"] = tables[0][13]
  result["a3_2_1"] = tables[0][14]
  result["a3_2_2"] = tables[0][15]
  result["a3_3_1"] = tables[0][16]
  result["a3_3_2"] = tables[0][17]
  result["a3_4"] = tables[0][18]
  result["a3_5"] = tables[0][19]
  result["a3_6_1"] = tables[0][20]
  result["a3_6_2"] = tables[0][21]
  result["a4_1"] = tables[0][22]
  result["a4_2"] = tables[0][23]
  result["a5_1"] = tables[0][24]
  result["a5_2"] = tables[0][25]
  result["a5_3"] = tables[0][26]
  


  return jsonify(result)





# Method : GET /getCustomerSurveyResult/<string:customer_name>
# Input : na
# Decription : get customer survey result by customer name 
@app.route('/getCustomerSurveyResult/<string:customer_name>')
def get_CustomerSurveyResult(customer_name):
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()


  

  catg_list = []
  question_list = {}
  catg_map = {}
  catg_idx = 0


  # prepare for workload survey

  workload_list = []
  

        
  catg_item = {}
  catg_item["catg_id"] = "q1"
  catg_item["catg_name"] = "Business Continuity by Top 5 Workload"
  catg_item["block_width"] = 12
  catg_item["layer"] = 2
  catg_item["subcatgs"] = []
  catg_list.append(catg_item)
  catg_map["q1"] = catg_idx
  catg_idx +=1 

  question_list["q1"] = []


  cursor.execute("select * from customer_workload where customer_name like '"+customer_name+"'")
  workloads = cursor.fetchall()

  cursor.execute("select * from workload_question_bank order by question_id")
  questions = cursor.fetchall()

  cursor.execute("select * from workload_survey where customer_name like '"+customer_name+"'")
  workload_survey_results = cursor.fetchall()
  if len(workload_survey_results) == 0 :
    for workload in workloads:
      cursor.execute('insert into workload_survey(customer_name, workload_id) values (?, ?)', [customer_name,workload[2]])
      conn.commit()
      cursor.execute("select * from workload_survey where customer_name like '"+customer_name+"'")
      workload_survey_results = cursor.fetchall()


  cursor.execute("select * from workload_survey_comment  where customer_name like '"+customer_name+"'")
  workload_survey_comments = cursor.fetchall()
  if len(workload_survey_comments) == 0 :
    for workload in workloads:
      cursor.execute('insert into workload_survey_comment(customer_name, workload_id) values (?, ?)', [customer_name,workload[2]])
      conn.commit()
      cursor.execute("select * from workload_survey_comment  where customer_name like '"+customer_name+"'")
      workload_survey_comments = cursor.fetchall()
  
  workload_result = {}
  workload_comment = {}

  for result in workload_survey_results:
    workload_id = result[1]
    r = {}
    r["summary"] = result[2]
    r["q1_1"] = result[3]
    r["q1_2"] = result[4]
    r["q1_3"] = result[5]
    r["q1_4"] = result[6]
    r["update_dt"] = result[7]

    workload_result[workload_id] = r
    # print(workload_result)

  for comment in workload_survey_comments:
    customer_name = comment[0]
    workload_id = comment[1]
    c = {}
    c["q1_1_desc"]    = comment[2]
    c["q1_1_action"]  = comment[3]
    c["q1_2_desc"]    = comment[4]
    c["q1_2_action"]  = comment[5]
    c["q1_3_desc"]    = comment[6]
    c["q1_3_action"]  = comment[7]
    c["q1_4_desc"]    = comment[8]
    c["q1_4_action"]  = comment[9]
    c["update_dt"] = comment[10]

    workload_comment[workload_id] = c

  workload_idx = 0

  for workload in workloads:
    w = {}
    workload_id = workload[2]
    w["workload_id"] = workload_id
    w["subcatg_name"] = workload[1]
    w["catg_desc_block"] = 1
    w["catg_desc_block_1"] = workload_result[workload_id]["summary"]
    w["items"] = []
    
    catg_list[0]["subcatgs"].append(w)


    

    for question in questions:
      question_id = question[1]
      q = {}
      
      q["question_id"] = question_id
      q["item_name"] = question[2]
      q["Data Source"] = question[3]
      q["Type"] = question[4]
      q["point_of_view"] = question[5]
      q["Rating"] = workload_result[workload_id][question_id]
      q["Rating_Definition"] = []
      q["Rating_Definition"].append({"rate":"5 stars", "value":5,"checked":False,"def":question[6]})
      q["Rating_Definition"].append({"rate":"4 stars", "value":4,"checked":False,"def":question[7]})
      q["Rating_Definition"].append({"rate":"3 stars", "value":3,"checked":False,"def":question[8]})
      q["Rating_Definition"].append({"rate":"2 stars", "value":2,"checked":False,"def":question[9]})
      q["Rating_Definition"].append({"rate":"1 stars", "value":1,"checked":False,"def":question[10]})
      

      rate_seq = 0
      for rate_def in q["Rating_Definition"]:
        if rate_def["rate"] == str(q["Rating"]) + " stars":
          q["Rating_Definition"][rate_seq]["checked"] = True
        rate_seq += 1  


      q["item_desc"] = workload_comment[workload_id][question_id+"_desc"]
      q["action"] = workload_comment[workload_id][question_id+"_action"]
      
      catg_list[0]["subcatgs"][workload_idx]["items"].append(q)


    workload_idx += 1



  # Prepare for customer survey
  cursor.execute("select * from customer_question_category order by catg_id")
  catgs = cursor.fetchall()

  for catg in catgs:
    catg_item = {}
    catg_item["catg_id"] = catg[0]
    catg_item["catg_name"] = catg[1]
    catg_item["catg_desc_block"] = 1
    catg_item["block_width"] = catg[2]
    catg_item["layer"] = 1
    catg_item["items"] = []
    catg_list.append(catg_item)
    catg_map[catg[0]] = catg_idx
    catg_idx +=1 

    question_list[catg[0]] = []

    
    
  cursor.execute("select * from customer_question_bank order by seq")
  questions = cursor.fetchall()
  

  for question in questions:

    catg_seq = catg_map[question[1]]
    print(catg_seq)
    
    q = {}
    q["question_id"] = question[2]
    q["item_name"] = question[3]
    q["Data Source"] = question[4]
    q["Type"] = question[5]
    q["point_of_view"] = question[6]
    q["Rating"] = 5
    q["Rating_Definition"] = []
    q["Rating_Definition"].append({"rate":"5 stars", "value":5,"checked":False,"def":question[7]})
    q["Rating_Definition"].append({"rate":"4 stars", "value":4,"checked":False,"def":question[8]})
    q["Rating_Definition"].append({"rate":"3 stars", "value":3,"checked":False,"def":question[9]})
    q["Rating_Definition"].append({"rate":"2 stars", "value":2,"checked":False,"def":question[10]})
    q["Rating_Definition"].append({"rate":"1 stars", "value":1,"checked":False,"def":question[11]})
    
    q["item_desc"] = ""
    q["action"] = ""

    catg_list[catg_seq]["items"].append(q)

    question_list[question[1]].append(question[2])
    
    
  
  


  cursor.execute("select * from customer_survey_result where customer_name = '"+customer_name+"'  and latest like 'Y'")
  tables = cursor.fetchall()
  print(tables)
  if len(tables) == 0 :
    cursor.execute('insert into customer_survey_result(customer_name) values (?)', [customer_name])
    conn.commit()
    cursor.execute("select * from customer_survey_result where customer_name = '"+customer_name+"'  and latest like 'Y'")
    tables = cursor.fetchall()

  result = {}

  result["customer_name"] = tables[0][0]
  result["q2_summary"] = tables[0][1]
  result["q2_1"] = tables[0][2]
  result["q2_2"] = tables[0][3]
  result["q3_summary"] = tables[0][4]
  result["q3_1"] = tables[0][5]
  result["q3_2"] = tables[0][6]
  result["q3_3"] = tables[0][7]
  result["q3_4"] = tables[0][8]
  result["q3_5"] = tables[0][9]
  result["q3_6"] = tables[0][10]
  result["q4_summary"] = tables[0][11]
  result["q4_1"] = tables[0][12]
  result["q4_2"] = tables[0][13]
  result["q5_summary"] = tables[0][14]
  result["q5_1"] = tables[0][15]
  result["q5_2"] = tables[0][16]
  result["q5_3"] = tables[0][17]
  result["q6_summary"] = ""
  result["q6_1"] = tables[0][18]
  result["q6_2"] = tables[0][19]
  result["q7_1"] = tables[0][20]
  result["q7_2"] = tables[0][21]
  result["q7_3"] = tables[0][22]
  result["q7_4"] = tables[0][23]
  result["q8_1"] = tables[0][24]
  result["q8_2"] = tables[0][25]
  result["q9_1"] = tables[0][26]
  result["q9_2"] = tables[0][27]
  result["q9_3"] = tables[0][28]
  result["q9_4"] = tables[0][29]
  result["update_dt"] = tables[0][30]
  result["latest"] = tables[0][31]

  result["q2_3"] = tables[0][32]
  # result["q2_3"] = ""
  # result["q2_3"] = ""
  # result["q2_3"] = ""

  cursor.execute("select * from customer_survey_comment where customer_name = '"+customer_name+"'")
  tables = cursor.fetchall()
  if len(tables) == 0 :
    cursor.execute('insert into customer_survey_comment(customer_name) values (?)', [customer_name])
    conn.commit()
    cursor.execute("select * from customer_survey_comment where customer_name = '"+customer_name+"'")
    tables = cursor.fetchall()

  comment = {}

  comment["customer_name"] = tables[0][0]
  comment["q2_1_desc"] = tables[0][1]
  comment["q2_1_action"] = tables[0][2]
  comment["q2_2_desc"] = tables[0][3]
  comment["q2_2_action"] = tables[0][4]
  comment["q3_1_desc"] = tables[0][5]
  comment["q3_1_action"] = tables[0][6]
  comment["q3_2_desc"] = tables[0][7]
  comment["q3_2_action"] = tables[0][8]
  comment["q3_3_desc"] = tables[0][9]
  comment["q3_3_action"] = tables[0][10]
  comment["q3_4_desc"] = tables[0][11]
  comment["q3_4_action"] = tables[0][12]
  comment["q3_5_desc"] = tables[0][13]
  comment["q3_5_action"] = tables[0][14]
  comment["q3_6_desc"] = tables[0][15]
  comment["q3_6_action"] = tables[0][16]
  comment["q4_1_desc"] = tables[0][17]
  comment["q4_1_action"] = tables[0][18]
  comment["q4_2_desc"] = tables[0][19]
  comment["q4_2_action"] = tables[0][20]
  comment["q5_1_desc"] = tables[0][21]
  comment["q5_1_action"] = tables[0][22]
  comment["q5_2_desc"] = tables[0][23]
  comment["q5_2_action"] = tables[0][24]
  comment["q5_3_desc"] = tables[0][25]
  comment["q5_3_action"] = tables[0][26]


  comment["q2_3_desc"] = tables[0][29]
  comment["q2_3_action"] = tables[0][30]
  # comment["q6_1_desc"] = tables[0][27]
  # comment["q6_1_action"] = tables[0][28]
  # comment["q6_2_desc"] = tables[0][29]
  # comment["q6_2_action"] = tables[0][30]
  # comment["q7_1_desc"] = tables[0][31]
  # comment["q7_1_action"] = tables[0][32]
  # comment["q7_2_desc"] = tables[0][33]
  # comment["q7_2_action"] = tables[0][34]
  # comment["q7_3_desc"] = tables[0][35]
  # comment["q7_3_action"] = tables[0][36]
  # comment["q7_4_desc"] = tables[0][37]
  # comment["q7_4_action"] = tables[0][38]
  # comment["q8_1_desc"] = tables[0][39]
  # comment["q8_1_action"] = tables[0][40]
  # comment["q8_2_desc"] = tables[0][41]
  # comment["q8_2_action"] = tables[0][42]
  # comment["q9_1_desc"] = tables[0][43]
  # comment["q9_1_action"] = tables[0][44]
  # comment["q9_2_desc"] = tables[0][45]
  # comment["q9_2_action"] = tables[0][46]
  # comment["q9_3_desc"] = tables[0][47]
  # comment["q9_3_action"] = tables[0][48]
  # comment["q9_4_desc"] = tables[0][49]
  # comment["q9_4_action"] = tables[0][50]
  # comment["update_dt"] = tables[0][51]
  # comment["latest"] = tables[0][52]

  for catg in catg_list:
    print(catg["catg_id"])
    catg_id = catg["catg_id"]
    catg_seq = catg_map[catg_id]

    if catg["layer"] == 1 :

      catg_list[catg_seq]["catg_desc_block_1"] = result[catg_id + "_summary"]

      question_idx = 0
      for question in question_list[catg_id]:
        question_id = catg_list[catg_seq]["items"][question_idx]["question_id"]

        if result[question_id] is None:
          catg_list[catg_seq]["items"][question_idx]["Rating"] = 0
        else:
          catg_list[catg_seq]["items"][question_idx]["Rating"] = result[question_id]

          rate_seq = 0
          for rate_def in catg_list[catg_seq]["items"][question_idx]["Rating_Definition"]:
            if rate_def["rate"] == str(result[question_id]) + " stars":
              catg_list[catg_seq]["items"][question_idx]["Rating_Definition"][rate_seq]["checked"] = True
            rate_seq += 1  


        if question_id+"_desc" in comment:
          catg_list[catg_seq]["items"][question_idx]["item_desc"] = comment[question_id+"_desc"]
          catg_list[catg_seq]["items"][question_idx]["action"] = comment[question_id+"_action"]

        question_idx += 1 

  result = {}
  result["categories"] = catg_list
  return jsonify(result)



# Method : GET /getCustomerESStatus/<string:customer_name>  
# Input : na
# Decription : get getCustomerESStatus
@app.route('/getCustomerESStatus/<string:customer_name>')
def getCustomerESStatus(customer_name):

  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  
  # cursor.execute("select c.*, s.* from customer_survey_overall s, customer_info c  where tam_1 like '"+tam_alias+"' and c.customer_name = s.customer_name")
  # tables = cursor.fetchall()

  # if len(tables) == 0 :
  cursor.execute("select * from customer_es_status_result where customer_name like '"+customer_name+"' and latest = 'Y' ")
  tables = cursor.fetchall()
  
  r = {}
  

  if len(tables) > 0 :
    for record in tables:
      r = {}
      r["q6_1"]           = record[1]
      r["q6_1_comment"]   = record[2]
      r["q6_1_update_dt"] = record[3]
      r["q6_2"]           = record[4]
      r["q6_2_comment"]   = record[5]
      r["q6_2_update_dt"] = record[6]
      r["q7_1"]           = record[7]
      r["q7_1_comment"]   = record[8]
      r["q7_1_update_dt"] = record[9]
      r["q7_2"]           = record[10]
      r["q7_2_comment"]   = record[11]
      r["q7_2_update_dt"] = record[12]
      r["q7_3"]           = record[13]
      r["q7_3_comment"]   = record[14]
      r["q7_3_update_dt"] = record[15]
      r["q7_4"]           = record[16]
      r["q7_4_comment"]   = record[17]
      r["q7_4_update_dt"] = record[18]
      r["q8_1"]           = record[19]
      r["q8_1_comment"]   = record[20]
      r["q8_1_update_dt"] = record[21]
      r["q8_2"]           = record[22]
      r["q8_2_comment"]   = record[23]
      r["q8_2_update_dt"] = record[24]
      r["q9_1"]           = record[25]
      r["q9_1_comment"]   = record[26]
      r["q9_1_update_dt"] = record[27]
      r["q9_2"]           = record[28]
      r["q9_2_comment"]   = record[29]
      r["q9_2_update_dt"] = record[30]
      r["q9_3"]           = record[31]
      r["q9_3_comment"]   = record[32]
      r["q9_3_update_dt"] = record[33]
      r["q9_4"]           = record[34]
      r["q9_4_comment"]   = record[35]
      r["q9_4_update_dt"] = record[36]
  else:
    r["q6_1"]           = ""
    r["q6_1_comment"]   = ""
    r["q6_1_update_dt"] = ""
    r["q6_2"]           = ""
    r["q6_2_comment"]   = ""
    r["q6_2_update_dt"] = ""
    r["q7_1"]           = ""
    r["q7_1_comment"]   = ""
    r["q7_1_update_dt"] = ""
    r["q7_2"]           = ""
    r["q7_2_comment"]   = ""
    r["q7_2_update_dt"] = ""
    r["q7_3"]           = ""
    r["q7_3_comment"]   = ""
    r["q7_3_update_dt"] = ""
    r["q7_4"]           = ""
    r["q7_4_comment"]   = ""
    r["q7_4_update_dt"] = ""
    r["q8_1"]           = ""
    r["q8_1_comment"]   = ""
    r["q8_1_update_dt"] = ""
    r["q8_2"]           = ""
    r["q8_2_comment"]   = ""
    r["q8_2_update_dt"] = ""
    r["q9_1"]           = ""
    r["q9_1_comment"]   = ""
    r["q9_1_update_dt"] = ""
    r["q9_2_comment"]   = ""
    r["q9_2_update_dt"] = ""
    r["q9_3"]           = ""
    r["q9_3_comment"]   = ""
    r["q9_3_update_dt"] = ""
    r["q9_4"]           = ""
    r["q9_4_comment"]   = ""
    r["q9_4_update_dt"] = ""
  
  
    




  return jsonify(r)

# Method : POST /updateCustomerSummary
# # Input : na
# # Decription : updateCustomerSummary

@app.route('/updateCustomerSummary', methods=['POST'])
def updateCustomerSummary():


  today = date.today().strftime("%Y-%m-%d")
  # uid = request.args.get('uid')
  customer_name = request.form['customer_name']

  summary = request.form['summary']

  if len(summary) == 0 :
    summary = "please summarize for the customer"
   
  print(customer_name  + ", "+ summary)    
  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  cursor.execute('update customer_survey_overall set summary = "'+summary+'" , update_dt = "'+today+'"  where customer_name like "'+customer_name+'"')
  conn.commit()
  result = {}
  result["result"] = "success"
  return jsonify(result)
 

# Method : POST /updateCatgSummary
# # Input : na
# # Decription : updateCatgSummary

@app.route('/updateCatgSummary', methods=['POST'])
def updateCatgSummary():

  today = date.today().strftime("%Y-%m-%d")
  # uid = request.args.get('uid')
  customer_name = request.form['customer_name']
  catg = request.form['catg_id']
  summary = request.form['summary']

  if len(summary) == 0 :
    summary = "please summarize for the survey result."
   
  print(customer_name + ", "+ catg + ", "+ summary)    
  
  workload_id = 0
  catg_id = catg
  if "_catg_" in catg:
    # workload + catg
    workload_id = catg.split("_catg_")[0].replace("w_","")
    catg_id = catg.split("_catg_")[1]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('update workload_survey set summary = "'+summary+'" , update_dt = "'+today+'"  where customer_name like "'+customer_name+'" and workload_id = ' + workload_id)
    conn.commit()

 
  else:
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('update customer_survey_result set '+catg_id+'_summary = "'+summary+'" where customer_name like "'+customer_name+'"  and latest like "Y"')
    conn.commit()

  result = {}
  result["result"] = "success"
  return jsonify(result)
    

# Method : POST /updateQuestionDesc
# # Input : na
# # Decription : updateQuestionDesc

@app.route('/updateQuestionDesc', methods=['POST'])
def updateQuestionDesc():


  today = date.today().strftime("%Y-%m-%d")
  # uid = request.args.get('uid')
  customer_name = request.form['customer_name']
  question = request.form['question_id']
  desc = request.form['desc']

  
  if "_q_" in question:

    workload_id = question.split("_q_")[0].replace("w_","")
    question_id = question.split("_q_")[1]
    print(customer_name)
    print(workload_id)
    print(question_id)
    print(desc)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('update workload_survey_comment set '+question_id+'_desc = "'+desc+'" , update_dt = "'+today+'"  where customer_name like "'+customer_name+'" and workload_id='+workload_id+'')
    conn.commit()
    
  else:
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('update customer_survey_comment set '+question+'_desc = "'+desc+'"  , update_dt = "'+today+'"  where customer_name like "'+customer_name+'"')
    conn.commit()
  # print(customer_name  + ", "+ summdescary)    
  
  if checkCompleteComment(customer_name):
    cursor.execute('update customer_survey_overall set complete_comment = "Yes"  where customer_name like "'+customer_name+'"')
    conn.commit()


  result = {}
  result["result"] = "success"
  return jsonify(result)
 

# Method : POST /updateQuestionAction
# # Input : na
# # Decription : updateQuestionAction

@app.route('/updateQuestionAction', methods=['POST'])
def updateQuestionAction():


  today = date.today().strftime("%Y-%m-%d")
  # uid = request.args.get('uid')
  customer_name = request.form['customer_name']
  question = request.form['question_id']
  action = request.form['action']

  
  if "_q_" in question:

    workload_id = question.split("_q_")[0].replace("w_","")
    question_id = question.split("_q_")[1]
    print(customer_name)
    print(workload_id)
    print(question_id)
    print(action)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('update workload_survey_comment set '+question_id+'_action = "'+action+'" , update_dt = "'+today+'"  where customer_name like "'+customer_name+'" and workload_id='+workload_id+'')
    conn.commit()
    
  else:
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('update customer_survey_comment set '+question+'_action = "'+action+'"  , update_dt = "'+today+'"  where customer_name like "'+customer_name+'"')
    conn.commit()
  # print(customer_name  + ", "+ summdescary)    
  
  if checkCompleteComment(customer_name):
    cursor.execute('update customer_survey_overall set complete_comment = "Yes"  where customer_name like "'+customer_name+'"')
    conn.commit()
  
  result = {}
  result["result"] = "success"
  return jsonify(result)




# Method : POST /updateQuestionScore
# # Input : na
# # Decription : updateQuestionScore

@app.route('/updateQuestionScore', methods=['POST'])
def updateQuestionScore():


  today = date.today().strftime("%Y-%m-%d")
  # uid = request.args.get('uid')
  customer_name = request.form['customer_name']
  question = request.form['question_id']
  score = request.form['score']

  
  today = date.today().strftime("%Y-%m-%d")
  if "_q_" in question:

    workload_id = question.split("_q_")[0].replace("w_","")
    question_id = question.split("_q_")[1]

    

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('update workload_survey set '+question_id+' = '+score+' , update_dt = "'+today+'" where customer_name like "'+customer_name+'" and workload_id='+workload_id+'')
    conn.commit()
    print('update workload_survey set '+question_id+' = '+score+' , update_dt = "'+today+'" where customer_name like "'+customer_name+'" and workload_id='+workload_id+'')
    cursor.execute('select * from workload_survey where customer_name like "'+customer_name+'"')
    workload_survey_results = cursor.fetchall()

    workload_sum = 0
    workload_count = 0
    workload_avg = 0

    for survey in workload_survey_results:
      workload_id = survey[1]
      
      q1_1 = survey[3]
      q1_2 = survey[4]
      q1_3 = survey[5]
      q1_4 = survey[6]
      if q1_1 :
        workload_sum += q1_1
        workload_count += 1
      if q1_2 :
        workload_sum += q1_2
        workload_count += 1
      if q1_3 :
        workload_sum += q1_3
        workload_count += 1
      if q1_4 :
        workload_sum += q1_4
        workload_count += 1

    if workload_count >0:
      workload_avg = workload_sum // workload_count

    cursor.execute('update customer_survey_overall set q1 = '+str(workload_avg)+' , update_dt = "'+today+'" where customer_name like "'+customer_name+'"')
    conn.commit()
    
  else:
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('update customer_survey_result set '+question+' = '+str(score)+', update_dt = "'+today+'"  where customer_name like "'+customer_name+'"  and latest like "Y"')
    conn.commit()

    workload_sum = 0
    workload_count = 0
    workload_avg = 0

  cursor.execute('select * from customer_survey_result where customer_name like "'+customer_name+'"  and latest like "Y"')
  survey_result = cursor.fetchall()

  store = {}
  for survey in survey_result:
    workload_id = survey[1]
    
    store["customer_name"] = survey[0]
    store["q2_summary"] = survey[1]
    store["q2_1"] = survey[2]
    store["q2_2"] = survey[3]
    store["q3_summary"] = survey[4]
    store["q3_1"] = survey[5]
    store["q3_2"] = survey[6]
    store["q3_3"] = survey[7]
    store["q3_4"] = survey[8]
    store["q3_5"] = survey[9]
    store["q3_6"] = survey[10]
    store["q4_summary"] = survey[11]
    store["q4_1"] = survey[12]
    store["q4_2"] = survey[13]
    store["q5_summary"] = survey[14]
    store["q5_1"] = survey[15]
    store["q5_2"] = survey[16]
    store["q5_3"] = survey[17]
    store["q6_summary"] = ""
    store["q6_1"] = survey[18]
    store["q6_2"] = survey[19]
    store["q7_1"] = survey[20]
    store["q7_2"] = survey[21]
    store["q7_3"] = survey[22]
    store["q7_4"] = survey[23]
    store["q8_1"] = survey[24]
    store["q8_2"] = survey[25]
    store["q9_1"] = survey[26]
    store["q9_2"] = survey[27]
    store["q9_3"] = survey[28]
    store["q9_4"] = survey[29]
    store["update_dt"] = survey[30]
    store["latest"] = survey[31]


  
  if "q2" in question:
    if store["q2_1"] :
      workload_sum += store["q2_1"]
      workload_count += 1
    if store["q2_2"] :
      workload_sum += store["q2_2"]
      workload_count += 1
  if "q3" in question:
    if store["q3_1"] :
      workload_sum += store["q3_1"]
      workload_count += 1
    if store["q3_2"] :
      workload_sum += store["q3_2"]
      workload_count += 1
    if store["q3_3"] :
      workload_sum += store["q3_3"]
      workload_count += 1
    if store["q3_4"] :
      workload_sum += store["q3_4"]
      workload_count += 1
    if store["q3_5"] :
      workload_sum += store["q3_5"]
      workload_count += 1
    if store["q3_6"] :
      workload_sum += store["q3_6"]
      workload_count += 1
  if "q4" in question:
    if store["q4_1"] :
      workload_sum += store["q4_1"]
      workload_count += 1
    if store["q4_2"] :
      workload_sum += store["q4_2"]
      workload_count += 1
  if "q5" in question:
    if store["q5_1"] :
      workload_sum += store["q5_1"]
      workload_count += 1
    if store["q5_2"] :
      workload_sum += store["q5_2"]
      workload_count += 1
    if store["q5_3"] :
      workload_sum += store["q5_3"]
      workload_count += 1
    

  if workload_count >0:
    workload_avg = workload_sum // workload_count

  cursor.execute('update customer_survey_overall set '+question.split("_")[0]+' = '+str(workload_avg)+' , update_dt = "'+today+'" where customer_name like "'+customer_name+'"')
  print('update customer_survey_overall set '+question.split("_")[0]+' = '+str(workload_avg)+' , update_dt = "'+today+'" where customer_name like "'+customer_name+'"')
  conn.commit()


  # print(customer_name  + ", "+ summdescary)    
    
  if checkCompleteSurvey(customer_name):
    cursor.execute('update customer_survey_overall set complete_survey = "Yes"  where customer_name like "'+customer_name+'"')
    conn.commit()
  
  result = {}
  result["result"] = "success"
  return jsonify(result)


def refreshOverallSummary(customer_name):
  today = date.today().strftime("%Y-%m-%d")
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  cursor.execute('select * from customer_survey_result where customer_name like "'+customer_name+'"  and latest like "Y"')
  survey_result = cursor.fetchall()

  workload_sum = 0
  workload_count = 0
  workload_avg = 0

  store = {}
  for survey in survey_result:
    
    store["customer_name"] = survey[0]
    store["q2_summary"] = survey[1]
    store["q2_1"] = survey[2]
    store["q2_2"] = survey[3]
    store["q3_summary"] = survey[4]
    store["q3_1"] = survey[5]
    store["q3_2"] = survey[6]
    store["q3_3"] = survey[7]
    store["q3_4"] = survey[8]
    store["q3_5"] = survey[9]
    store["q3_6"] = survey[10]
    store["q4_summary"] = survey[11]
    store["q4_1"] = survey[12]
    store["q4_2"] = survey[13]
    store["q5_summary"] = survey[14]
    store["q5_1"] = survey[15]
    store["q5_2"] = survey[16]
    store["q5_3"] = survey[17]
    store["q6_summary"] = ""
    store["q6_1"] = survey[18]
    store["q6_2"] = survey[19]
    store["q7_1"] = survey[20]
    store["q7_2"] = survey[21]
    store["q7_3"] = survey[22]
    store["q7_4"] = survey[23]
    store["q8_1"] = survey[24]
    store["q8_2"] = survey[25]
    store["q9_1"] = survey[26]
    store["q9_2"] = survey[27]
    store["q9_3"] = survey[28]
    store["q9_4"] = survey[29]
    store["update_dt"] = survey[30]
    store["latest"] = survey[31]

  questions = ["q2","q3","q4","q5"]

  for question in questions:

    if "q2" in question:
      if store["q2_1"] :
        workload_sum += store["q2_1"]
        workload_count += 1
      if store["q2_2"] :
        workload_sum += store["q2_2"]
        workload_count += 1
    if "q3" in question:
      if store["q3_1"] :
        workload_sum += store["q3_1"]
        workload_count += 1
      if store["q3_2"] :
        workload_sum += store["q3_2"]
        workload_count += 1
      if store["q3_3"] :
        workload_sum += store["q3_3"]
        workload_count += 1
      if store["q3_4"] :
        workload_sum += store["q3_4"]
        workload_count += 1
      if store["q3_5"] :
        workload_sum += store["q3_5"]
        workload_count += 1
      if store["q3_6"] :
        workload_sum += store["q3_6"]
        workload_count += 1
    if "q4" in question:
      if store["q4_1"] :
        workload_sum += store["q4_1"]
        workload_count += 1
      if store["q4_2"] :
        workload_sum += store["q4_2"]
        workload_count += 1
    if "q5" in question:
      if store["q5_1"] :
        workload_sum += store["q5_1"]
        workload_count += 1
      if store["q5_2"] :
        workload_sum += store["q5_2"]
        workload_count += 1
      if store["q5_3"] :
        workload_sum += store["q5_3"]
        workload_count += 1
      

    if workload_count >0:
      workload_avg = workload_sum // workload_count

    cursor.execute('update customer_survey_overall set '+question+' = '+str(workload_avg)+' , update_dt = "'+today+'" where customer_name like "'+customer_name+'"')
    print('update customer_survey_overall set '+question+' = '+str(workload_avg)+' , update_dt = "'+today+'" where customer_name like "'+customer_name+'"')
    conn.commit()


def checkCompleteSurvey(customer_name):
  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  # customer survey
  cursor.execute('select * from customer_survey_result where customer_name like "'+customer_name+'"  and latest like "Y"')
  survey_result = cursor.fetchall()


  for survey in survey_result:
    
    survey_idx_list = [2,3,5,6,7,8,9,10,12,13,15,16,17]

    for survey_idx in survey_idx_list:
      if survey[survey_idx] is None:
        print("customer survey is not complete, id = "+ str(survey_idx))
        return False

  # workload survey
  cursor.execute('select * from workload_survey where customer_name like "'+customer_name+'"  and latest like "Y"')
  survey_result = cursor.fetchall()

  for survey in survey_result:
    print("survey")
    print(survey)
    
    survey_idx_list = [3,4,5,6]

    for survey_idx in survey_idx_list:
      if survey[survey_idx] is None:
        print("workload survey is not complete, id = "+ str(survey_idx))
        return False

  return True


def checkCompleteComment(customer_name):
  print("check complete comment")
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
    
  # catg_sum
  cursor.execute('select * from customer_survey_result where customer_name like "'+customer_name+'" and latest like "Y"')
  survey_result = cursor.fetchall()
  
  for survey in survey_result:
    survey_idx_list = [1,4,11,14]

    for survey_idx in survey_idx_list:
      if survey[survey_idx] is None:
        print(survey)
        return False

  # item_desc and action
  cursor.execute('select * from customer_survey_comment where customer_name like "'+customer_name+'"  and latest like "Y"')
  survey_result = cursor.fetchall()

  for survey in survey_result:
    
    for item in survey:
      if survey is None:
        print(item)
        return False


  # workload sum
  cursor.execute('select * from workload_survey where customer_name like "'+customer_name+'"')
  survey_result = cursor.fetchall()

  for survey in survey_result:
    
    survey_idx_list = [2]

    for survey_idx in survey_idx_list:
      if survey[survey_idx] is None:
        print(survey)
        return False


  # item_desc and action
  cursor.execute('select * from workload_survey_comment where customer_name like "'+customer_name+'"')
  survey_result = cursor.fetchall()

  for survey in survey_result:
    
    for item in survey:
      if survey is None:
        print(survey)
        return False



  return True



# Method : POST /addWorkload
# # Input : na
# # Decription : addWorkload


# Method : POST /addCustomer
# # Input : na
# # Decription : addCustomer

# @app.route('/addCustomer', methods=['POST'])
# # def addCustomer():

  
#   today = date.today().strftime("%Y-%m-%d")
#   # uid = request.args.get('uid')
#   customer_name = request.form['customer_name']
#   customer_domain = request.form['customer_domain']
#   tam_alias = request.form['tam_alias']
#   permission = checkUserPermission(tam_alias)

  
  
#   conn = sqlite3.connect(DATABASE)
#   cursor = conn.cursor()

  
#   cursor.execute("select * from customer_info where customer_name like '"+customer_name+"'")
#   tables = cursor.fetchall()
  
#   if len(tables) > 0:

#     result = {}
#     result["result"] = "fail"
#     result["message"] = "Add customer failed. The customer name is duplicate with exist workload. (customer domain: "+tables[0][6] +" , tam: "+ tables[0][1] + " )"
#     return jsonify(result)
  
#   else:
    
    
#     cursor.execute('insert into customer_info(customer_name, tam_1, customer_domain, poc) values (?, ?,?,?)', [customer_name,tam_alias,customer_domain, permission])
#     conn.commit()
#     cursor.execute('insert into customer_survey_overall(customer_name, summary,tamalias) values (?, ?,?)', [customer_name,"please input TAM's summary for the customer",tam_alias])
#     conn.commit()
#     cursor.execute('insert into customer_workload(customer_name) values (?)', [customer_name])
#     conn.commit()
  

#   result = {}
#   result["result"] = "Success create customer: "+ customer_name
#   return jsonify(result)
 
# Method : POST /addWorkload
# # Input : na
# # Decription : addWorkload

@app.route('/addWorkload', methods=['POST'])
def addWorkload():


  today = date.today().strftime("%Y-%m-%d")
  # uid = request.args.get('uid')
  customer_name = request.form['customer_name']
  workload_name = request.form['workload_name']

  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()

  
  cursor.execute("select * from customer_workload where customer_name like '"+customer_name+"' and workload_name like '"+workload_name+"'")
  tables = cursor.fetchall()
  
  if len(tables) > 0:
    result = {}
    result["result"] = "fail"
    result["message"] = "Add workload failed. The workload name is duplicate with exist workload."
    return jsonify(result)
  
  else:
    
    cursor.execute('insert into customer_workload(customer_name, workload_name) values (?, ?)', [customer_name,workload_name])
    conn.commit()
    
  

  result = {}
  result["result"] = "success"
  return jsonify(result)
 

# Method : POST /addWorkload
# # Input : na
# # Decription : addWorkload

@app.route('/changeWorkloadName', methods=['POST'])
def changeWorkloadName():


  today = date.today().strftime("%Y-%m-%d")
  # uid = request.args.get('uid')
  customer_name = request.form['customer_name']
  workload_name = request.form['workload_name']
  workload_id = request.form['workload_id']

  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()

  
  # cursor.execute("select * from customer_workload where customer_name like '"+customer_name+"' and workload_name like '"+workload_name+"'")
  # tables = cursor.fetchall()
  
  # if len(tables) > 0:
  #   result = {}
  #   result["result"] = "fail"
  #   result["message"] = "Add workload failed. The workload name is duplicate with exist workload."
  #   return jsonify(result)
  
  # else:
    
  cursor.execute('update customer_workload set workload_name = "'+workload_name+'" where customer_name like "'+customer_name+'" and workload_id = '+workload_id)
  conn.commit()
    
  

  result = {}
  result["result"] = "success"
  return jsonify(result)
 

# Method : POST /updateWorkload
# # Input : na
# # Decription : updateWorkload

@app.route('/updateWorkload', methods=['POST'])
def updateWorkload():


  today = date.today().strftime("%Y-%m-%d")
  # uid = request.args.get('uid')
  customer_name = request.form['customer_name']
  workload_id = request.form['workload_name']
  new_workload_name = request.form['newworkload_name']

  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()

  

  cursor.execute(cursor.execute('update customer_workload set workload_name = "'+new_workload_name+'"   where customer_name like "'+customer_name+'" and workload_id = '+workload_id))
  conn.commit()
    
  

  result = {}
  result["result"] = "success"
  return jsonify(result)



# Method : POST /submitSurvey
# # Input : na
# # Decription : submitSurvey

@app.route('/submitSurvey', methods=['POST'])
def submitSurvey():

  
  today = date.today().strftime("%Y-%m-%d")
  # uid = request.args.get('uid')
  customer_name = request.form['customer_name']
  es_type = request.form['es_type']
  q1 = json.loads(request.form['q_1'])
  q2_1 = request.form['q_2_1']
  q2_2 = request.form['q_2_2']
  a2_1 = request.form['a_2_1']
  a2_2 = request.form['a_2_2'].rstrip(',')
  q3_1 = request.form['q_3_1']
  q3_2 = request.form['q_3_2']
  q3_3 = request.form['q_3_3']
  q3_4 = request.form['q_3_4']
  q3_5 = request.form['q_3_5']
  q3_6 = request.form['q_3_6']
  a3_1 = request.form['a_3_1']
  a3_2_1 = request.form['a_3_2_1']
  a3_2_2 = request.form['a_3_2_2']
  a3_3_1 = request.form['a_3_3_1']
  a3_3_2 = request.form['a_3_3_2']
  a3_4 = request.form['a_3_4']
  a3_5 = request.form['a_3_5'].rstrip(',')
  a3_6_1 = request.form['a_3_6_1']
  a3_6_2 = request.form['a_3_6_2'].rstrip(',')

  q4_1 = request.form['q_4_1']
  q4_2 = request.form['q_4_2']
  a4_1 = request.form['a_4_1'].rstrip(',')
  a4_2 = request.form['a_4_2'].rstrip(',')

  q5_1 = request.form['q_5_1']
  q5_2 = request.form['q_5_2']
  q5_3 = request.form['q_5_3']
  a5_1 = request.form['a_5_1'].rstrip(',')
  a5_2 = request.form['a_5_2'].rstrip(',')
  a5_3 = request.form['a_5_3'].rstrip(',')


  q2_summary = ""
  q3_summary = ""
  q4_summary = ""
  q5_summary = ""

  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()


  # update customer survey answer
  cursor.execute("select * from customer_survey_answer where customer_name like '"+customer_name+"' and latest like 'Y'")
  tables = cursor.fetchall()
  
  if len(tables) > 0:
    
    cursor.execute('update customer_survey_answer set latest="N" where customer_name like "'+customer_name+'" and latest like "Y"')
    conn.commit()

  cursor.execute('insert into customer_survey_answer(customer_name, a2_1,a2_2,'
    + ' a3_1,a3_2_1,a3_2_2,a3_3_1,a3_3_2,a3_4,a3_5,a3_6_1,a3_6_2,'
    + ' a4_1,a4_2,'
    + ' a5_1,a5_2,a5_3,'
    + ' update_dt) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', [customer_name,a2_1,a2_2,a3_1,a3_2_1,a3_2_2,a3_3_1,a3_3_2,a3_4,a3_5,a3_6_1,a3_6_2,a4_1,a4_2,a5_1,a5_2,a5_3,today])
  conn.commit()




  # update customer survey result
  cursor.execute("select * from customer_survey_result where customer_name like '"+customer_name+"' and latest like 'Y'")
  tables = cursor.fetchall()
  
  if len(tables) > 0:
    # result = {}
    # result["result"] = "fail"
    # result["message"] = "Add workload failed. The workload name is duplicate with exist workload."
    # return jsonify(result)

    q2_summary = tables[0][1]
    q3_summary = tables[0][14]
    q4_summary = tables[0][11]
    q5_summary = tables[0][14]

    cursor.execute('update customer_survey_result set latest="N" where customer_name like "'+customer_name+'" and latest like "Y"')
    conn.commit()
  
  
    
  cursor.execute('insert into customer_survey_result(customer_name, q2_summary, q2_1,q2_2,'
    + ' q3_summary,q3_1,q3_2,q3_3,q3_4,q3_5,q3_6,'
    + ' q4_summary,q4_1,q4_2,'
    + ' q5_summary,q5_1,q5_2,q5_3,'
    + ' update_dt) values (?, ?,?,?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', [customer_name,q2_summary,q2_1,q2_2,q3_summary,q3_1,q3_2,q3_3,q3_4,q3_5,q3_6,q4_summary,q4_1,q4_2,q5_summary,q5_1,q5_2,q5_3,today])
  conn.commit()
  
  # update customer survey comment
  cursor.execute("select * from customer_survey_comment where customer_name like '"+customer_name+"' and latest like 'Y'")
  tables = cursor.fetchall()

  if len(tables) == 0:
    cursor.execute('insert into customer_survey_comment(customer_name,update_dt) values (?,?)', [customer_name,today])
    conn.commit()

  # print(q1)
  workload_sum = 0
  workload_count = 0
  workload_avg = 0

  

    
  for workload in q1["list"]:
    workload_id = workload['workload_id']
    q1_1 = workload['q1_1']
    q1_2 = workload['q1_2']
    q1_3 = workload['q1_3']
    q1_4 = 0
    if 'q1_4' in workload:
      q1_4 = workload['q1_4']

    a1_1 = workload['a1_1'].rstrip(',')
    a1_2 = workload['a1_2'].rstrip(',')
    a1_3 = workload['a1_3'].rstrip(',')
    a1_4 = 0
    if 'a1_4' in workload:
      a1_4 = workload['a1_4']


    if q1_1 :
      workload_sum += q1_1
      workload_count += 1
    if q1_2 :
      workload_sum += q1_2
      workload_count += 1
    if q1_3 :
      workload_sum += q1_3
      workload_count += 1
    if int(q1_4) > 0:
      workload_sum += int(q1_4)
      workload_count += 1

    print("work sum = " + str(workload_sum))
    print("work count = " + str(workload_count))
    # update workload answer

    print("select * from workload_survey_answer where customer_name like '"+customer_name+"' and workload_id = "+workload_id+" and latest like 'Y'")
    cursor.execute("select * from workload_survey_answer where customer_name like '"+customer_name+"' and workload_id = "+workload_id+" and latest like 'Y'")

    tables = cursor.fetchall()
    
    if len(tables) > 0:

      cursor.execute('update workload_survey_answer set latest="N" where customer_name like "'+customer_name+'" and workload_id = '+workload_id+'  and latest like "Y"')
      conn.commit()
    
          
    cursor.execute('insert into workload_survey_answer(customer_name, workload_id,a1_1,a1_2,a1_3,a1_4,update_dt) values (?,?,?,?,?,?,?)', [customer_name,workload_id,a1_1,a1_2,a1_3,a1_4,today])
    conn.commit()



    # update workload survey 
    q1_summary = ""

    cursor.execute("select * from workload_survey where customer_name like '"+customer_name+"' and workload_id = "+workload_id+" and latest like 'Y'")
    tables = cursor.fetchall()
    
    if len(tables) > 0:
      q1_summary = tables[0][2]

      cursor.execute('update workload_survey set latest="N" where customer_name like "'+customer_name+'" and workload_id = '+workload_id+'  and latest like "Y"')
      conn.commit()
      print('update workload_survey set latest="N" where customer_name like "'+customer_name+'" and workload_id = '+workload_id+'  and latest like "Y"')
    
          
    cursor.execute('insert into workload_survey(customer_name, workload_id,summary,q1_1,q1_2,q1_3,q1_4,update_dt) values (?,?,?,?,?,?,?,?)', [customer_name,workload_id,q1_summary,q1_1,q1_2,q1_3,q1_4,today])
    conn.commit()




    cursor.execute('update customer_survey_overall set q1 = '+str(workload_avg)+' , update_dt = "'+today+'" where customer_name like "'+customer_name+'"')
    conn.commit()

    # update workload survey comment
    cursor.execute("select * from workload_survey_comment where customer_name like '"+customer_name+"' and workload_id = "+workload_id+" and latest like 'Y'")
    tables = cursor.fetchall()

    if len(tables) == 0:
      cursor.execute('insert into workload_survey_comment(customer_name, workload_id,update_dt) values (?,?,?)', [customer_name,workload_id,today])
      conn.commit()



  if workload_count >0:
    workload_avg = workload_sum // workload_count    
    cursor.execute('update customer_survey_overall set q1 = "'+str(workload_avg)+'"  where customer_name like "'+customer_name+'"')
    conn.commit()
  print("workload_avg = " + str(workload_avg))
  

  cursor.execute('update customer_info set es_type = "'+es_type+'"  where customer_name like "'+customer_name+'" ')
  conn.commit()


  if checkCompleteSurvey(customer_name):
    cursor.execute('update customer_survey_overall set complete_survey = "Yes"  where customer_name like "'+customer_name+'"')
    conn.commit()

  refreshOverallSummary(customer_name)

  cursor.execute('update customer_info set es_type = "'+es_type+'"  where customer_name like "'+customer_name+'" ')
  conn.commit()



  result = {}
  result["result"] = "success"
  return jsonify(result)



# Method : POST /updateCustomerSummary
# # Input : na
# # Decription : updateCustomerSummary

@app.route('/updateCustomerESStatus', methods=['POST'])
def updateCustomerESStatus():


  today = date.today().strftime("%Y-%m-%d")
  # uid = request.args.get('uid')
  customer_name = request.form['customer_name']
  question_id = request.form['question_id']
  answer = request.form['answer']
  comment = request.form['comment']
  update_dt = today

  if not answer:
    answer = ""

  if not comment:
    comment = ""
  
  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()

  cursor.execute("select * from customer_es_status_result where customer_name like '"+customer_name+"' and latest like 'Y'")
  tables = cursor.fetchall()
  if len(tables) == 0 :
    cursor.execute('insert into customer_es_status_result(customer_name, '+question_id+', '+question_id+'_comment, '+question_id+'_update_dt) values (?, ?, ?, ?)', [customer_name,answer,comment,update_dt])
    conn.commit()
  else:
    cursor.execute('update customer_es_status_result set '+question_id+' = "'+answer+'" , '+question_id+'_comment = "'+comment+'", '+question_id+'_update_dt = "'+update_dt+'"   where customer_name like "'+customer_name+'"')
    conn.commit()
  result = {}
  result["result"] = "success"
  return jsonify(result)
 



# Method : GET /getCustomerSentiment
# # Input : na
# # Decription : getCustomerSentiment

@app.route('/getCustomerExperience/<string:customer_name>', methods=['GET'])
def getCustomerExperience(customer_name):

  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()
  today = date.today().strftime("%Y-%m-%d")
  update_dt = today

  cursor.execute("select * from customer_experience where customer_name like '"+customer_name+"' and latest = 'Y'")
  tables = cursor.fetchall()
  if len(tables) == 0 :
    cursor.execute('insert into customer_experience(customer_name, update_dt ) values (?, ?)', [customer_name,update_dt])
    conn.commit()
 
  cursor.execute("select * from customer_experience where customer_name like '"+customer_name+"' and latest = 'Y'")
  tables = cursor.fetchall()


  result = {}
  result["update_dt"] = tables[0][1]
  result["sentiment"] = tables[0][2]
  result["summary"] = tables[0][3]



  return jsonify(result)
 

# Method : POST /updateSentiment
# # Input : na
# # Decription : updateSentiment

@app.route('/updateSentiment', methods=['POST'])
def updateSentiment():


  today = date.today().strftime("%Y-%m-%d")
  # uid = request.args.get('uid')
  customer_name = request.form['customer_name']
  score = request.form['score']
  update_dt = today

  summary = "please input comment for the customer experience."

  
  conn = sqlite3.connect(DATABASE)
  cursor = conn.cursor()

  cursor.execute("select * from customer_experience where customer_name like '"+customer_name+"' and latest = 'Y'")
  tables = cursor.fetchall()
  if len(tables) == 0 :
    cursor.execute('insert into customer_experience(customer_name, sentiment, update_dt ) values (?, ?,?)', [customer_name,score,update_dt])
    conn.commit()
  else:
    summary = tables[0][3]
    cursor.execute('update customer_experience set latest = "N"   where customer_name like "'+customer_name+'" and latest = "Y"')
    conn.commit()

    cursor.execute('insert into customer_experience(customer_name, sentiment, update_dt, sentiment_summary ) values (?, ?,?,?)', [customer_name,score,update_dt,summary])
    conn.commit()
  result = {}
  result["result"] = "success"
  return jsonify(result)




if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=8080)
