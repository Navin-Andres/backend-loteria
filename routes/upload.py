"""
Upload Blueprint
Handles Excel file uploads and historical data processing
"""
from flask import Blueprint, jsonify, request
import pandas as pd
from database import get_db_connection
from pathlib import Path
import os

upload_bp = Blueprint('upload', __name__, url_prefix='/api')


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


def load_historical_data(file_path='baloto1.xlsx'):
    """Load and process historical data from Excel file"""
    try:
        df = pd.read_excel(file_path, sheet_name='Hoja1')
        print(f"Loaded DataFrame: {df.shape}")
        
        if df.empty:
            raise Exception("Archivo Excel vacío")
        
        def parse_resultado(resultado):
            """Parse resultado string into list of numbers"""
            numbers = [int(num.strip()) for num in str(resultado).split('-')]
            if len(numbers) != 6:
                raise ValueError(f"Formato inválido: se esperan 6 números, se encontraron {len(numbers)}")
            if not all(1 <= num <= 43 for num in numbers[:5]):
                raise ValueError("Los primeros 5 números deben estar entre 1 y 43")
            if not 1 <= numbers[5] <= 16:
                raise ValueError("El sexto número debe estar entre 1 y 16")
            return numbers
        
        df['balotas'] = df['resultado'].apply(parse_resultado)
        print(f"After parsing: {len(df)} rows processed")
        
        if 'balotas' in df.columns and not df['balotas'].empty:
            df[['balota1', 'balota2', 'balota3', 'balota4', 'balota5', 'balota6']] = pd.DataFrame(
                df['balotas'].tolist(), 
                index=df.index
            )
        else:
            print("No 'balotas' column or data available")
            return pd.DataFrame()
        
        return df
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return pd.DataFrame()


@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """Upload and process Excel file with historical lottery data"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.endswith('.xlsx'):
        return jsonify({'error': 'Invalid file format. Only .xlsx files are allowed'}), 400
    
    # Save file
    file_path = Path(__file__).parent.parent / 'baloto1.xlsx'
    file.save(str(file_path))
    
    # Load data into SQLite
    try:
        df = load_historical_data(str(file_path))
        
        if not df.empty:
            conn = get_db_connection()
            
            # Clear existing historical data
            c = execute_query(conn, 'DELETE FROM historical_data')
            
            # Insert new data
            for _, row in df.iterrows():
                c = execute_query(
                    conn,
                    '''INSERT INTO historical_data 
                       (balota1, balota2, balota3, balota4, balota5, balota6) 
                       VALUES (?, ?, ?, ?, ?, ?)''',
                    (int(row['balota1']), int(row['balota2']), int(row['balota3']), 
                     int(row['balota4']), int(row['balota5']), int(row['balota6']))
                )
            
            conn.commit()
            conn.close()
            
            print(f"✅ Successfully loaded {len(df)} records into database")
            return jsonify({
                'message': 'File uploaded successfully',
                'records': len(df)
            }), 200
        else:
            return jsonify({'error': 'No valid data found in Excel file'}), 400
            
    except Exception as e:
        print(f"Error loading data: {e}")
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500
