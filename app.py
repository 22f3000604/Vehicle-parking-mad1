from flask import Flask,url_for,request,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login", methods = ['GET', 'POST'])
def login():
    return render_template('login.html')

if __name__ ==  "__main__":
    app.run(debug = True,port = 8080)


