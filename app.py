from flask import Flask
from flask_mysqldb import MySQL
from config import mydb
from views import login, home, reserve, room, billing, employee

app = Flask(__name__)

app.secret_key = '12345678'

mysql = MySQL(app)

app.register_blueprint(login.bp)
app.register_blueprint(home.bp)
app.register_blueprint(reserve.bp)
app.register_blueprint(room.bp)
app.register_blueprint(billing.bp)
app.register_blueprint(employee.bp)



if __name__ == "__main__":
    app.run()