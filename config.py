import MySQLdb

MYSQL_DATABASE_HOST = '127.0.0.1'
MYSQL_DATABASE_USER = 'root'
MYSQL_DATABASE_PASSWORD = 'root'
MYSQL_DATABASE_DB = 'hotel'
SECRET_DATABASE_KEY = '12345678'

mydb = MySQLdb.connect(host=MYSQL_DATABASE_HOST,
                       user=MYSQL_DATABASE_USER,
                       passwd=MYSQL_DATABASE_PASSWORD,
                       db=MYSQL_DATABASE_DB)