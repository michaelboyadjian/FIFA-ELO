from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MySQL_HOST'] = 'HOST'
app.config['MySQL_USER'] = 'USER'
app.config['MySQL_PASSWORD'] = 'PASSWORD'
app.config['MySQL_DB'] = 'DB'

mysql = MySQL(app)

@app.route('/')
def index():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Rankings")
        mysql.connection.commit()
        cur.close()
        rval = cur.fetchall()
        return str(rval)

if __name__ == '__main__':
    app.run(debug=True)