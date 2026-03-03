from flask import Blueprint, request
from app.auth.service import send_otp_service, verify_otp_service
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/send-otp", methods=["POST"])
def send_otp():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return {"error": "Email is required"}, 400

    return send_otp_service(email)


@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")

    if not email or not otp:
        return {"error": "Email and OTP required"}, 400

    return verify_otp_service(email, otp)


# Protected route test
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    current_user = get_jwt_identity()
    return {
        "message": "Token valid",
        "email": current_user
    }, 200