from flask import Blueprint, request, jsonify, current_app
from database import db
from models.user import User
import jwt
from datetime import datetime, timedelta

users_bp = Blueprint('users', __name__)
SECRET = 'super-secret-key-change-me'

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({'message': 'username, email and password required'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'email already registered'}), 400
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'user registered', 'user': user.to_dict()}), 201

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'message': 'email and password required'}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'invalid credentials'}), 401
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    return jsonify({'token': token})