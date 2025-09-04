from flask import Flask, url_for, request, render_template, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from datetime import datetime, timedelta
from flask_migrate import Migrate
from models.file import db, User, Admin, ParkingLot, ParkingSpot, ReservationParkingSpot
from email_utils import generate_verification_token, send_verification_email, send_welcome_email
from config import Config

from flask_mail import Mail, Message
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "QuickPark"

# Load email configuration
app.config.from_object(Config)

#email verification and otp generation
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'QUICKPARK101@gmail.com'
app.config['MAIL_PASSWORD'] = 'mnoy oypd fnyd sbkm'
app.config['MAIL_DEFAULT_SENDER'] = "QUICKPARK101@gmail.com"
 
mail = Mail(app)

otp_storage = {}

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(email, otp):
    msg = Message(  
        "Quick Park - Authentication",
        recipients=[email],
        body=f"Welcome to Quick Park. Your one time Authentication Password is: {otp}. This OTP is valid for 5 minutes"
    )
    mail.send(msg)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

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
            if not user.is_verified:
                flash('Please verify your email before logging in.', 'error')
                return redirect(url_for('verify_email', email=user.email))
            
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

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please use a different email or login.')
            return render_template('signup.html', error='Email already exists')

        # Generate verification token
        verification_token = generate_verification_token()
        
        hashed_password = generate_password_hash(password)
        # Create user but don't verify yet
        new_user = User(
            name=username, 
            email=email, 
            phone=phone, 
            password=hashed_password,
            is_verified=False
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generate and send OTP
        otp = generate_otp()
        otp_storage[email] = otp
        send_otp_email(email, otp)
        
        flash('Account created! Please check your email for verification OTP.', 'success')
        return redirect(url_for('verify_email', email=email))
    
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
    
    reservations = ReservationParkingSpot.query.filter_by(user_id=user.id)\
        .order_by(ReservationParkingSpot.parking_timestamp.desc()).all()
    
    return render_template('dashboard.html', user=user, parking_lots=parking_lots, reservations=reservations)

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    if request.method == 'POST':
        email = request.form.get('email')
        entered_otp = request.form.get('otp')
        
        if email in otp_storage and otp_storage[email] == entered_otp:
            user = User.query.filter_by(email=email).first()
            if user:
                user.is_verified = True
                db.session.commit()
                del otp_storage[email]
                flash('Email verified successfully! You can now login.', 'success')
                return redirect(url_for('login'))
        else:
            flash('Invalid OTP. Please try again.', 'error')
    
    email = request.args.get('email', '')
    return render_template('verify_email.html', email=email)

@app.route('/resend-otp', methods=['POST'])
def resend_otp():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    
    if user and not user.is_verified:
        otp = generate_otp()
        otp_storage[email] = otp
        send_otp_email(email, otp)
        flash('OTP resent successfully!', 'success')
    
    return redirect(url_for('verify_email', email=email))

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
@login_required
def summary():
    user = User.query.get(session['user_id'])
    reservations = ReservationParkingSpot.query.filter_by(user_id=user.id).all()
    return render_template('summary.html', user=user, reservations=reservations)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
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

        if not all([prime_location_name, address, pin_code, price, max_spots]):
            flash('All fields are required!')
            return render_template('add_lot.html')

        try:
            max_spots = int(max_spots)
            price = float(price)
        except ValueError:
            flash('Invalid price or max spots value!')
            return render_template('add_lot.html')

        new_lot = ParkingLot(
            prime_location_name=prime_location_name,
            address=address,
            pin_code=pin_code,
            price=price,
            maximum_number_of_spots=max_spots
        )
        
        db.session.add(new_lot)
        db.session.commit()

        for i in range(max_spots):
            spot = ParkingSpot(lot_id=new_lot.id, status='available')
            db.session.add(spot)
        
        db.session.commit()

        flash(f'Parking lot "{prime_location_name}" with {max_spots} spots added successfully!')
        return redirect(url_for('add_lot'))
    
    return render_template('add_lot.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            return redirect(url_for('add_lot'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    return render_template('admin_login.html')

@app.route('/book_lot/<int:lot_id>', methods=['GET', 'POST'])
@login_required
def book_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    available_spots = ParkingSpot.query.filter_by(lot_id=lot_id, status='available').all()
    
    if request.method == 'POST':
        spot_id = request.form.get('spot_id')
        start_date = request.form.get('start_date')
        start_time = request.form.get('start_time')
        duration = request.form.get('duration')
        
        if not all([spot_id, start_date, start_time, duration]):
            flash('Please fill in all required fields.', 'error')
            return render_template('book_lot.html', lot=lot, available_spots=available_spots, today=datetime.now().strftime('%Y-%m-%d'))
        
        try:
            start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
            duration_hours = int(duration)
            end_datetime = start_datetime + timedelta(hours=duration_hours)
            
            if start_datetime <= datetime.now():
                flash('Booking time must be in the future.', 'error')
                return render_template('book_lot.html', lot=lot, available_spots=available_spots, today=datetime.now().strftime('%Y-%m-%d'))
            
            spot = ParkingSpot.query.get(spot_id)
            if not spot or spot.status != 'available':
                flash('Selected parking spot is no longer available.', 'error')
                return render_template('book_lot.html', lot=lot, available_spots=available_spots, today=datetime.now().strftime('%Y-%m-%d'))
            
            overlapping = ReservationParkingSpot.query.filter(
                ReservationParkingSpot.spot_id == spot_id,
                ReservationParkingSpot.end_time > start_datetime,
                ReservationParkingSpot.start_time < end_datetime
            ).first()
            
            if overlapping:
                flash('This spot is already booked for the selected time period.', 'error')
                return render_template('book_lot.html', lot=lot, available_spots=available_spots, today=datetime.now().strftime('%Y-%m-%d'))
            
            total_cost = duration_hours * 50
            
            reservation = ReservationParkingSpot(
                user_id=session['user_id'],
                spot_id=spot_id,
                start_time=start_datetime,
                end_time=end_datetime,
                parking_timestamp=datetime.now(),
                total_cost=total_cost,
                duration_hours=duration_hours
            )
            
            db.session.add(reservation)
            db.session.commit()
            
            flash(f'Parking spot booked successfully! Total cost: ₹{total_cost}', 'success')
            return redirect(url_for('dashboard'))
            
        except ValueError:
            flash('Invalid date or time format.', 'error')
            return render_template('book_lot.html', lot=lot, available_spots=available_spots, today=datetime.now().strftime('%Y-%m-%d'))
    
    return render_template('book_lot.html', lot=lot, available_spots=available_spots, today=datetime.now().strftime('%Y-%m-%d'))

def create_sample_data():
    """Create sample data for testing - only runs once"""
    # Check if data already exists
    if Admin.query.first() is None:
        # Create admin
        admin = Admin(
            username='admin',
            password=generate_password_hash('admin123')
        )
        db.session.add(admin)
        
        # Create sample user
        sample_user = User(
            name='pooja',
            email='pooja@example.com',
            phone='1234567890',
            password=generate_password_hash('password123'),
            is_verified=True
        )
        db.session.add(sample_user)
        
        # Create multiple parking locations
        locations = [
            {
                'name': 'Central Mall',
                'address': '123 Main Street, City Center',
                'pin': '123456',
                'spots': 10
            },
            {
                'name': 'Airport Parking',
                'address': '456 Airport Road',
                'pin': '654321',
                'spots': 20
            },
            {
                'name': 'Gandhi Chowk',
                'address': 'Gandhi Chowk, Main Market Area',
                'pin': '110001',
                'spots': 15
            },
            {
                'name': 'Saili Road',
                'address': 'Saili Road, Near City Hospital',
                'pin': '110002',
                'spots': 12
            },
            {
                'name': 'Metro Station',
                'address': 'Metro Station Complex, Platform 1',
                'pin': '110003',
                'spots': 25
            },
            {
                'name': 'City Plaza',
                'address': 'City Plaza, Shopping District',
                'pin': '110004',
                'spots': 18
            }
        ]
        
        # Create parking lots
        for location in locations:
            lot = ParkingLot(
                prime_location_name=location['name'],
                price=50.0,
                address=location['address'],
                pin_code=location['pin'],
                maximum_number_of_spots=location['spots']
            )
            db.session.add(lot)
        
        db.session.commit()
        
        # Create parking spots for each lot
        all_lots = ParkingLot.query.all()
        for lot in all_lots:
            for i in range(1, lot.maximum_number_of_spots + 1):
                spot = ParkingSpot(lot_id=lot.id, status='available')
                db.session.add(spot)
        
        db.session.commit()
        print("Sample data created successfully!")

# Create tables and sample data on first run
with app.app_context():
    db.create_all()
    create_sample_data()

if __name__ == '__main__':
    app.run(debug=True)

