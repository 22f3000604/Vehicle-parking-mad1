from flask import Flask, url_for, request, render_template, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from models.file import db, User, Admin, ParkingLot, ParkingSpot, ReservationParkingSpot


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "QuickPark"


db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.session.query(User).filter_by(name=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
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



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to login first')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function




@app.route("/dashboard")
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    parking_lots = ParkingLot.query.all()
    reservations = ReservationParkingSpot.query.filter_by(user_id=user.id).order_by(ReservationParkingSpot.parking_timestamp.desc()).all()
    return render_template('dashboard.html', user=user, parking_lots=parking_lots, reservations=reservations)

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/Aboutus')
def Aboutus():
    return render_template('Aboutus.html')

@app.route('/Contact')
def Contact():
    return render_template('Contact.html')

@app.route('/Carrer')
def Carrer():
    return render_template('Carrer.html')

@app.route('/summary')
def summary():
    user = User.query.get(session['user_id'])
    reservations = ReservationParkingSpot.query.filter_by(user_id=user.id).all()
    return render_template('summary.html', user=user, reservations=reservations)

@app.route('/edit_profile', methods=['GET', 'POST'])
def editprofile():
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.email = request.form.get('email')
        user.phone = request.form.get('phone')
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('dashboard'))
    return render_template('edit_profile.html', user=user)

@app.route('/admin/add_lot', methods=['GET', 'POST'])
@admin_required
def add_lot():
    if request.method == 'POST':
        prime_location_name = request.form.get('prime_location_name')
        address = request.form.get('address')
        pin_code = request.form.get('pin_code')
        price = request.form.get('price')
        max_spots = request.form.get('max_spots')

        new_lot = ParkingLot(
            prime_location_name=prime_location_name,
            address=address,
            pin_code=pin_code,
            price=float(price),
            maximum_number_of_spots=int(max_spots)
        )
        db.session.add(new_lot)
        db.session.commit()
        for i in range(max_spots):
            spot = ParkingSpot(lot_id=new_lot.id, status='available')
            db.session.add(spot)
        db.session.commit()


        flash('Parking lot added successfully!')
        return redirect(url_for('add_parking_lot'))
    return render_template('add_lot.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            return redirect(url_for('add_parking_lot'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    return render_template('admin_login.html')

@app.route('/book_lot/<int:lot_id>')
@login_required
def book_lot(lot_id):
    user_id = session['user_id']
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='available').first()
    if not spot:
        flash('No available spots in this lot.')
        return redirect(url_for('dashboard'))
    spot.status = 'booked'
    reservation = ReservationParkingSpot(
        spot_id=spot.id,
        user_id=user_id,
        parking_timestamp=datetime.utcnow(),
        parking_cost_per_unit_time=spot.parking_lot.price
    )
    db.session.add(reservation)
    db.session.commit()
    flash(f'Successfully booked spot {spot.id} in lot {spot.parking_lot.prime_location_name}!')
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()                                
        if not Admin.query.filter_by(username='admin').first():
                admin = Admin(username='admin', password=generate_password_hash('yourpassword'))
                db.session.add(admin)
                db.session.commit()
    app.run(debug=True,port= 5000)