from flask import Flask,url_for,request,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ ==  "__main__":
    app.run(debug = True)


