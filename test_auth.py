"""
Script de prueba para el sistema de autenticación
Crea un usuario de prueba y verifica el login
"""
import requests
import json

BASE_URL = 'http://192.168.1.9:8080'

def test_register():
    """Prueba el registro de usuario"""
    print("🔵 Probando registro...")
    response = requests.post(
        f'{BASE_URL}/api/register',
        headers={'Content-Type': 'application/json'},
        json={'username': 'test_user', 'password': 'test1234'}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_login():
    """Prueba el login de usuario"""
    print("🔵 Probando login...")
    response = requests.post(
        f'{BASE_URL}/api/login',
        headers={'Content-Type': 'application/json'},
        json={'username': 'test_user', 'password': 'test1234'}
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    
    if data.get('success'):
        print(f"✅ Login exitoso! User ID: {data.get('user_id')}")
        return data.get('user_id')
    else:
        print("❌ Login falló")
        return None

def test_save_sorteo(user_id):
    """Prueba guardar un sorteo"""
    print("🔵 Probando guardar sorteo...")
    response = requests.post(
        f'{BASE_URL}/api/save_sorteo',
        headers={'Content-Type': 'application/json'},
        json={
            'user_id': user_id,
            'numbers': [5, 12, 23, 34, 42, 8]
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_get_history(user_id):
    """Prueba obtener el historial"""
    print("🔵 Probando obtener historial...")
    response = requests.get(f'{BASE_URL}/api/history/{user_id}')
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    print()

if __name__ == '__main__':
    print("=" * 50)
    print("PRUEBAS DEL SISTEMA DE AUTENTICACIÓN")
    print("=" * 50)
    print()
    
    # Primero intenta registrar (puede fallar si ya existe)
    try:
        test_register()
    except Exception as e:
        print(f"⚠️ Registro falló (usuario puede ya existir): {e}")
        print()
    
    # Login
    user_id = test_login()
    
    if user_id:
        # Guardar sorteo
        test_save_sorteo(user_id)
        
        # Obtener historial
        test_get_history(user_id)
    
    print("=" * 50)
    print("✅ PRUEBAS COMPLETADAS")
    print("=" * 50)
