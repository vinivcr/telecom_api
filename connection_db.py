import pymysql

# Conectando ao banco de dados AWS RDS
def get_connection():
  return pymysql.connect(
  host='15.228.100.136',
  user='telecom_user',
  password='4Wb42T%zkG6Q',
  database='telecom_db',
  cursorclass=pymysql.cursors.DictCursor
                         )
