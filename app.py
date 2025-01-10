from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", titolo="Home")

@app.route("/login")
def login():
    return render_template("login.html", titolo="login")

@app.route("/register")
def register():
    return render_template("register.html", titolo="register")



app.run(debug=True)
