from flask_mail import Message
from flask import current_app, url_for
import secrets
import string

def generate_verification_token():
    """Generate a secure random token for email verification"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(32))

def send_verification_email(mail, user_email, user_name, verification_token):
    """Send verification email to user"""
    try:
        verification_link = url_for('verify_email', token=verification_token, _external=True)
        
        msg = Message(
            subject='Verify Your Email - QuickPark',
            recipients=[user_email],
            html=f'''
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%); padding: 20px; border-radius: 10px;">
                    <h2 style="color: #2b5876; text-align: center;">Welcome to QuickPark!</h2>
                    
                    <div style="background: white; padding: 30px; border-radius: 8px; margin: 20px 0;">
                        <h3>Hi {user_name},</h3>
                        <p>Thank you for signing up with QuickPark! To complete your registration and start booking parking spots, please verify your email address.</p>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{verification_link}" 
                               style="background-color: #1e90ff; color: white; padding: 12px 30px; 
                                      text-decoration: none; border-radius: 8px; font-weight: bold;
                                      display: inline-block;">
                                Verify Email Address
                            </a>
                        </div>
                        
                        <p>If the button doesn't work, copy and paste this link into your browser:</p>
                        <p style="word-break: break-all; color: #1e90ff;">{verification_link}</p>
                        
                        <p style="margin-top: 30px; color: #666;">
                            If you didn't create an account with QuickPark, please ignore this email.
                        </p>
                    </div>
                    
                    <p style="text-align: center; color: #666; font-size: 12px;">
                        © 2025 QuickPark. All rights reserved.
                    </p>
                </div>
            </body>
            </html>
            ''',
            body=f'''
            Hi {user_name},
            
            Thank you for signing up with QuickPark!
            
            To complete your registration, please verify your email address by clicking the link below:
            {verification_link}
            
            If you didn't create an account with QuickPark, please ignore this email.
            
            Best regards,
            QuickPark Team
            '''
        )
        
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

def send_welcome_email(mail, user_email, user_name):
    """Send welcome email after successful verification"""
    try:
        login_link = url_for('login', _external=True)
        
        msg = Message(
            subject='Welcome to QuickPark - Email Verified!',
            recipients=[user_email],
            html=f'''
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%); padding: 20px; border-radius: 10px;">
                    <h2 style="color: #2b5876; text-align: center;">Email Verified Successfully! 🎉</h2>
                    
                    <div style="background: white; padding: 30px; border-radius: 8px; margin: 20px 0;">
                        <h3>Hi {user_name},</h3>
                        <p>Congratulations! Your email has been successfully verified. You can now access all QuickPark features:</p>
                        
                        <ul style="color: #333; line-height: 1.6;">
                            <li>🅿️ Find and book parking spots instantly</li>
                            <li>📱 Manage your reservations</li>
                            <li>💰 Transparent pricing in INR</li>
                            <li>🔒 Secure and safe parking</li>
                        </ul>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{login_link}" 
                               style="background-color: #10b981; color: white; padding: 12px 30px; 
                                      text-decoration: none; border-radius: 8px; font-weight: bold;
                                      display: inline-block;">
                                Login to QuickPark
                            </a>
                        </div>
                        
                        <p style="margin-top: 30px; color: #666;">
                            Start your hassle-free parking experience today!
                        </p>
                    </div>
                    
                    <p style="text-align: center; color: #666; font-size: 12px;">
                        © 2025 QuickPark. All rights reserved.
                    </p>
                </div>
            </body>
            </html>
            ''',
            body=f'''
            Hi {user_name},
            
            Congratulations! Your email has been successfully verified.
            
            You can now login and start booking parking spots: {login_link}
            
            Welcome to QuickPark!
            
            Best regards,
            QuickPark Team
            '''
        )
        
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Failed to send welcome email: {str(e)}")
        return False
