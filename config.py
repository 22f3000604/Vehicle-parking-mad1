import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Email configuration for Gmail SMTP
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    
    # Set these environment variables or replace with your actual values
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Your Gmail address
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Your Gmail App Password
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')
    
    # App Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'QuickPark')
    
    # Base URL for email links
    BASE_URL = os.environ.get('BASE_URL', 'http://127.0.0.1:5173')
    
    # Alternative: SendGrid configuration (uncomment to use SendGrid instead)
    # MAIL_SERVER = 'smtp.sendgrid.net'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = 'apikey'
    # MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
    # MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')
