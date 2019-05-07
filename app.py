from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL

app = Flask(__name__)
Bootstrap(app)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['myql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/post')
def post():
    return render_template('post.html')

if __name__ == '__main__':
    app.run()