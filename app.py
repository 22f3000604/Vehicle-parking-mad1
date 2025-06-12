from flask import Flask,url_for,request,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
 
from models.file import User, Admin, ParkingLot,ReservationParkingSpot
with app.app_context():
    db.create_all()
    print("Database created successfully!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.session.query(User).filter_by(name=username).first()
        if user and check_password_hash(user.password, password):
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')       


@app.route("/signup", methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        hashed_password = generate_password_hash(password)
        new_user = User(name=username, email=email, phone=phone, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('signup.html')

        
        

if __name__ ==  "__main__":
    app.run(debug = True,)


