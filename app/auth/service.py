import random
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from app.extensions import db, bcrypt
from app.models import OTPVerification
from app.utils.email import send_email


OTP_EXPIRY_MINUTES = 5


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_service(email):
    # Delete old OTPs for this email
    OTPVerification.query.filter_by(email=email).delete()

    otp = generate_otp()
    otp_hash = bcrypt.generate_password_hash(otp).decode("utf-8")

    expires_at = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)

    otp_entry = OTPVerification(
        email=email,
        otp_hash=otp_hash,
        expires_at=expires_at,
        attempts=0,
        created_at=datetime.utcnow(),
    )

    db.session.add(otp_entry)
    db.session.commit()

    # Send email
    send_email(
        subject="Your OTP Code",
        recipients=[email],
        body=f"Your OTP is {otp}. It expires in {OTP_EXPIRY_MINUTES} minutes.",
    )

    return {"message": "OTP sent successfully"}, 200


def verify_otp_service(email, otp_input):
    otp_entry = OTPVerification.query.filter_by(email=email).first()

    if not otp_entry:
        return {"error": "OTP not found"}, 400

    if otp_entry.expires_at < datetime.utcnow():
        return {"error": "OTP expired"}, 400

    if otp_entry.attempts >= 5:
        return {"error": "Too many attempts"}, 400

    if not bcrypt.check_password_hash(otp_entry.otp_hash, otp_input):
        otp_entry.attempts += 1
        db.session.commit()
        return {"error": "Invalid OTP"}, 400

    # OTP valid → delete it
    db.session.delete(otp_entry)
    db.session.commit()

    access_token = create_access_token(identity=email)

    return {
        "message": "Login successful",
        "token": access_token
    }, 200