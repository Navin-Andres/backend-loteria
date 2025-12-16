"""
Lottery Blueprint
Handles lottery generation, history, and statistics
"""
from flask import Blueprint, jsonify, request
from database import get_db_connection
import random
from collections import Counter
import os

lottery_bp = Blueprint('lottery', __name__, url_prefix='/api')


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


def get_top_3_frequent():
    """Get the top 3 most frequent numbers from historical data"""
    try:
        conn = get_db_connection()
        c = execute_query(conn, 'SELECT COUNT(*) FROM historical_data')
        count = c.fetchone()[0]
        
        if count > 0:
            # Get frequency of each number from all balota columns (1-5 only)
            numbers = []
            for i in range(1, 6):
                c = execute_query(conn, f'SELECT balota{i} FROM historical_data')
                numbers.extend([row[0] for row in c.fetchall()])
            
            conn.close()
            
            # Count frequency
            counter = Counter(numbers)
            top_3 = [num for num, _ in counter.most_common(3)]
            return top_3 if len(top_3) == 3 else random.sample(range(1, 44), 3)
        else:
            conn.close()
            return random.sample(range(1, 44), 3)
    except Exception as e:
        print(f"Error getting top 3 frequent: {e}")
        return random.sample(range(1, 44), 3)


@lottery_bp.route('/sorteo', methods=['GET'])
def sorteo():
    """Generate a new lottery sorteo"""
    top_three = get_top_3_frequent()
    
    # Use top three as the first three balotas, then add three random from remaining numbers
    available_numbers = [x for x in range(1, 44) if x not in top_three]
    three_random = random.sample(available_numbers, 3)  # Three unique random numbers
    all_five_balotas = top_three + three_random
    random.shuffle(all_five_balotas)  # Shuffle to randomize order
    
    sixth_balota = random.randint(1, 16)  # Extra balota (1-16)
    balotas = all_five_balotas
    balotas.append(sixth_balota)  # Ensure exactly 6 numbers
    
    print(f"Generated balotas: {balotas}")  # Debug print
    
    if not (1 <= sixth_balota <= 16):
        print(f"Warning: Sixth balota {sixth_balota} is out of range 1-16")
    
    return jsonify({'balotas': balotas})


@lottery_bp.route('/save_sorteo', methods=['POST'])
def save_sorteo():
    """Save a sorteo to user's history"""
    data = request.json
    user_id = data.get('user_id')
    numbers = data.get('numbers')
    
    if not user_id or not numbers:
        return jsonify({'error': 'Missing data'}), 400
    
    conn = get_db_connection()
    c = execute_query(
        conn,
        'INSERT INTO sorteos (user_id, numbers) VALUES (?, ?)', 
        (user_id, ','.join(map(str, numbers)))
    )
    conn.commit()
    conn.close()
    
    return jsonify({'success': True}), 200


@lottery_bp.route('/history/<int:user_id>', methods=['GET'])
def get_history(user_id):
    """Get user's sorteo history"""
    conn = get_db_connection()
    c = execute_query(
        conn,
        'SELECT id, numbers, created_at FROM sorteos WHERE user_id = ? ORDER BY created_at DESC', 
        (user_id,)
    )
    rows = c.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        numbers = [int(n) for n in row[1].split(',')]
        history.append({
            'id': row[0],
            'numbers': numbers,
            'date': str(row[2])
        })
    
    return jsonify({'history': history}), 200


@lottery_bp.route('/statistics', methods=['GET'])
def statistics():
    """Get lottery statistics (top 3 most frequent numbers with count)"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM historical_data')
        count = c.fetchone()[0]
        
        if count > 0:
            # Get frequency of each number from all balota columns (1-5 only)
            numbers = []
            for i in range(1, 6):
                c.execute(f'SELECT balota{i} FROM historical_data')
                numbers.extend([row[0] for row in c.fetchall()])
            
            conn.close()
            
            # Count frequency and get top 3
            counter = Counter(numbers)
            top_3_with_count = counter.most_common(3)
            
            # Format response
            top_numbers = [
                {'number': num, 'count': freq} 
            execute_query(conn, 'SELECT COUNT(*) FROM historical_data')
        count = c.fetchone()[0]
        
        if count > 0:
            # Get frequency of each number from all balota columns (1-5 only)
            numbers = []
            for i in range(1, 6):
                c = execute_query(conn, ing statistics: {e}")
        return jsonify({'top_three_numbers': []})


@lottery_bp.route('/sorteo/<int:sorteo_id>', methods=['DELETE'])
def delete_sorteo(sorteo_id):
    """Delete a sorteo by ID"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.exexecute_query(conn, 'DELETE FROM sorteos WHERE id = ?', (sorteo_id,))
        conn.commit()
        
        # rowcount funciona en ambas bases de datos
        rows_affected = c.rowcount
        conn.close()
        
        if rows_affectedonify({'error': 'Sorteo not found'}), 404
        
        return jsonify({'success': True, 'message': 'Sorteo deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lottery_bp.route('/sorteo/<int:sorteo_id>', methods=['PUT'])
def update_sorteo(sorteo_id):
    """Update a sorteo by ID"""
    try:
        data = request.json
        numbers = data.get('numbers')
        
        if not numbers or len(numbers) != 6:
            return jsonify({'error': 'Invalid numbers format'}), 400
        
        # Validate numbers
        for i in range(5):
            if not (1 <= numbers[i] <= 43):
                return jsonify({'error': f'Number {i+1} must be between 1-43'}), 400
        if not (1 <= numbers[5] <= 16):
            return jsonify({'error': 'Sixth number must be between 1-16'}), 400
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            'UPDATE sorteos SET numbers = ? WHERE id = ?', 
            (','.join(map(str, numbers)), sorteo_id)
        )
        conn.commit()
        conn.close()
        
        if c.rowcount == 0:
            return jsonify({'error': 'Sorteo not found'}), 404
        
        return jsonify({'success': True, 'message': 'Sorteo updated'}), 200
    except Exception as e:
        retuexecute_query(
            conn,
            'UPDATE sorteos SET numbers = ? WHERE id = ?', 
            (','.join(map(str, numbers)), sorteo_id)
        )
        conn.commit()
        
        rows_affected = c.rowcount
        conn.close()
        
        if rows_affected