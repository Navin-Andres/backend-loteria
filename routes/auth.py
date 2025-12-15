"""
Authentication Blueprint
Handles user registration and login
"""
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
import sqlite3

auth_bp = Blueprint('auth', __name__, url_prefix='/api')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({
            'success': False, 
            'message': 'Usuario y contraseña requeridos'
        }), 400
    
    conn = get_db_connection()
    c = conn.cursor()
    
    try:
        hashed_password = generate_password_hash(password)
        c.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)', 
            (username, hashed_password)
        )
        conn.commit()
        return jsonify({
            'success': True, 
            'message': 'Usuario registrado exitosamente'
        }), 200
    except sqlite3.IntegrityError:
        return jsonify({
            'success': False, 
            'message': 'El usuario ya existe'
        }), 400
    finally:
        conn.close()


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate a user"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({
            'success': False, 
            'message': 'Usuario y contraseña requeridos'
        }), 400
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id, password FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    
    if user and check_password_hash(user[1], password):
        return jsonify({
            'success': True, 
            'user_id': user[0], 
            'message': 'Login exitoso'
        }), 200
    else:
        return jsonify({
            'success': False, 
            'message': 'Usuario o contraseña incorrectos'
        }), 401
