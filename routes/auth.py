"""
Authentication Blueprint
Handles user registration and login
"""
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/api')


def execute_query(conn, query, params=()):
    """Execute query with appropriate placeholder for DB type"""
    database_url = os.getenv('DATABASE_URL', '')
    is_postgres = database_url.startswith('postgres')
    
    if is_postgres:
        # PostgreSQL usa %s
        query = query.replace('?', '%s')
    
    c = conn.cursor()
    c.execute(query, params)
    return c


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
    
    try:
        hashed_password = generate_password_hash(password)
        c = execute_query(
            conn,
            'INSERT INTO users (username, password) VALUES (?, ?)', 
            (username, hashed_password)
        )
        conn.commit()
        return jsonify({
            'success': True, 
            'message': 'Usuario registrado exitosamente'
        }), 200
    except Exception as e:
        # Maneja tanto IntegrityError de SQLite como psycopg2
        if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
            return jsonify({
                'success': False, 
                'message': 'El usuario ya existe'
            }), 400
        else:
            return jsonify({
                'success': False, 
                'message': f'Error: {str(e)}'
            }), 500
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
    c = execute_query(conn, 'SELECT id, password FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    
    if user:
        # Maneja tanto SQLite Row como PostgreSQL tuple
        user_id = user[0] if isinstance(user, tuple) else user['id']
        user_password = user[1] if isinstance(user, tuple) else user['password']
        
        if check_password_hash(user_password, password):
            return jsonify({
                'success': True, 
                'user_id': user_id, 
                'message': 'Login exitoso'
            }), 200
    
    return jsonify({
        'success': False, 
        'message': 'Usuario o contraseña incorrectos'
    }), 401
