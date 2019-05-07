from flask import Flask, render_template, request, redirect, session, url_for
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml
import os

app = Flask(__name__)
Bootstrap(app)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = request.form
        name = form['name']
        email = form['email']
        age = form['age']
        password = form['pass']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(name, email, age, password) VALUES(%s, %s, %s, %s)",
            (name, age, age, password))
        mysql.connection.commit()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'name' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        form = request.form
        name = form['your_name']
        password = form['your_pass']
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(1) FROM user WHERE name = %s;", [name])
        if cur.fetchone()[0]:
            cur.execute("SELECT password FROM user WHERE name = %s;", [name])
            for row in cur.fetchall():
                if password == row[0]:
                    session['name'] = form['your_name']
                    return redirect(url_for('index'))
                else:
                    error = "Invalid Credential."
        else:
            error = "Invalid Credential."
    return render_template('login.html', error=error)

@app.route('/post')
def post():
    return render_template('post.html')

if __name__ == '__main__':
    app.run()