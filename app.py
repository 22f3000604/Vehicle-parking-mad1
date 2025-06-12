from flask import Flask,url_for,request,render_template,redirect,session,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash,generate_password_hash
from functools import wraps
from models.file import db, User, Admin, ParkingLot, ParkingSpot, ReservationParkingSpot

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
            return redirect(url_for('dashboard'))
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


app.secret_key = "QuickPark"
def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if 'user_id' not in session:
            flash('you need to login first')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function    

@app.route("/dashboard", )
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html',user = user)

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))
        

if __name__ ==  "__main__":
    app.run(debug=True, port=8080)


