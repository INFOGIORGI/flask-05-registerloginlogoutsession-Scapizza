from flask import Flask,render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['MYSQL_HOST']="138.41.20.102"
app.config['MYSQL_PORT']=53306
app.config['MYSQL_USER']="ospite"
app.config['MYSQL_PASSWORD']='ospite'
app.config['MYSQL_DB']="w3schools"
app.secret_key="yabadabadu"
mysql= MySQL(app)

@app.route("/")
def home():
    return render_template("index.html", titolo="Home")

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "GET":
        return render_template("register.html", titolo="register")
    
    fname = request.form.get('fname', "")
    lname = request.form.get('lname', "")
    username = request.form.get('username', "") 
    password = request.form.get('password', "")
    confirm_password = request.form.get('confirm_password',"")
    
    cursor=mysql.connection.cursor()
    errore=""
    query="SELECT * FROM users WHERE username=%s"
    cursor.execute(query, (username,))
    
    if password!=confirm_password: errore="password diverse"

    elif len(cursor.fetchall())==1: errore="username esistente" 
    
    else:
        query="INSERT INTO users VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (username, generate_password_hash(password), fname, lname))
        mysql.connection.commit()
        cursor.execute("SELECT * FROM users")
        print(cursor.fetchall())
        return redirect(url_for("home"))

    flash(errore)
    return redirect(url_for("register"))
    
    
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method=="GET":
        return render_template("login.html", titolo="login")
    
    username=request.form.get("username", "")
    password=request.form.get("password", "")
    
    cursor=mysql.connection.cursor()
    
    query="SELECT username FROM users WHERE username=%s"
    cursor.execute(query, (username,))
    
    if len(cursor.fetchall())==1 and check_password_hash(generate_password_hash(password), password):
        return redirect(url_for("home"))
    
    flash("credenziali non valide")
    return redirect(url_for("login"))
    


app.run(debug=True)
