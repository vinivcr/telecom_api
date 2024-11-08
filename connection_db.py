import pymysql

# Conectando ao banco de dados AWS RDS
def get_connection():
  return pymysql.connect(
  host='localhost',
  user='telecom_user',
  password='%c$hDWW4pmDo',
  database='telecom_db',
  cursorclass=pymysql.cursors.DictCursor
                         )
