from __init__ import app
from flaskext.mysql import MySQL

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'proyectosis'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)