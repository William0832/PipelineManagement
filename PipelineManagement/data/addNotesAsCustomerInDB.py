import json, os, sqlite3

root_dir = os.path.abspath(os.path.dirname(__file__))
jsonPath = os.path.join(root_dir, 'json','notes.json')
dbPath = os.path.join(root_dir, 'production_database.db')

# preset cols in DB
inputCols = [
  'customer_id', 'id', 'customer', 'markpoint', 'stamp', 'testing', 'data', 'previousData', 'package', 'contact'
]

# load json
with open(jsonPath, 'r', encoding='utf8') as f:
  data = f.read()
data = json.loads(data)

# connect DB
conn = sqlite3.connect(dbPath)
c = conn.cursor()

# create table and init cols
colsStr = ''
for e in inputCols:
  temp = ''
  if e == 'customer_id':
    temp = e + ' PRIMARY KEY,'
  else:
    temp = e + ' TEXT,'
  colsStr += temp
sqlStr = f'CREATE TABLE IF NOT EXISTS customer ({colsStr[:-1]});'
conn.execute(sqlStr)

# add data to DB by loop
questions = ('?,'*len(inputCols))[:-1]
sql = f'INSERT INTO customer VALUES ({questions})'
n = 0
for e in data:
  n += 1
  list = [n]
  for k in inputCols:
    if k != 'customer_id':
      list.append(e[k])
  c.execute(sql, (list))
  conn.commit()
conn.close()


