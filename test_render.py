"""
Script para probar el backend desplegado en Render
"""
import requests
import json
import sys

# Cambia esta URL por la de tu deployment en Render
BASE_URL = input("Ingresa la URL de tu backend en Render (ej: https://sorteo-loteria-api.onrender.com): ")
BASE_URL = BASE_URL.rstrip('/')

print("\n" + "="*60)
print("🧪 PROBANDO BACKEND EN RENDER")
print("="*60)
print(f"URL Base: {BASE_URL}")
print("="*60 + "\n")

def test_health():
    """Probar health check"""
    print("1️⃣  Probando Health Check...")
    try:
        response = requests.get(f'{BASE_URL}/health', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {data.get('message', 'OK')}")
            return True
        else:
            print(f"   ❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_register():
    """Probar registro"""
    print("\n2️⃣  Probando Registro de Usuario...")
    try:
        response = requests.post(
            f'{BASE_URL}/api/register',
            headers={'Content-Type': 'application/json'},
            json={'username': 'test_user_render', 'password': 'test1234'},
            timeout=10
        )
        data = response.json()
        if response.status_code == 200 and data.get('success'):
            print(f"   ✅ {data.get('message', 'Registro exitoso')}")
            return True
        elif response.status_code == 400 and 'ya existe' in data.get('message', ''):
            print(f"   ⚠️  Usuario ya existe (esto es normal)")
            return True
        else:
            print(f"   ❌ Error: {data.get('message', 'Error desconocido')}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_login():
    """Probar login"""
    print("\n3️⃣  Probando Login...")
    try:
        response = requests.post(
            f'{BASE_URL}/api/login',
            headers={'Content-Type': 'application/json'},
            json={'username': 'test_user_render', 'password': 'test1234'},
            timeout=10
        )
        data = response.json()
        if response.status_code == 200 and data.get('success'):
            user_id = data.get('user_id')
            print(f"   ✅ Login exitoso - User ID: {user_id}")
            return user_id
        else:
            print(f"   ❌ Error: {data.get('message', 'Error desconocido')}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def test_sorteo():
    """Probar generación de sorteo"""
    print("\n4️⃣  Probando Generación de Sorteo...")
    try:
        response = requests.get(f'{BASE_URL}/api/sorteo', timeout=10)
        if response.status_code == 200:
            data = response.json()
            balotas = data.get('balotas', [])
            if len(balotas) == 6:
                print(f"   ✅ Sorteo generado: {balotas}")
                return balotas
            else:
                print(f"   ❌ Formato incorrecto: {balotas}")
                return None
        else:
            print(f"   ❌ Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def test_save_sorteo(user_id, numbers):
    """Probar guardar sorteo"""
    print("\n5️⃣  Probando Guardar Sorteo...")
    try:
        response = requests.post(
            f'{BASE_URL}/api/save_sorteo',
            headers={'Content-Type': 'application/json'},
            json={'user_id': user_id, 'numbers': numbers},
            timeout=10
        )
        if response.status_code == 200:
            print(f"   ✅ Sorteo guardado correctamente")
            return True
        else:
            print(f"   ❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_history(user_id):
    """Probar obtener historial"""
    print("\n6️⃣  Probando Obtener Historial...")
    try:
        response = requests.get(f'{BASE_URL}/api/history/{user_id}', timeout=10)
        if response.status_code == 200:
            data = response.json()
            history = data.get('history', [])
            print(f"   ✅ Historial obtenido: {len(history)} sorteos")
            return True
        else:
            print(f"   ❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_statistics():
    """Probar estadísticas"""
    print("\n7️⃣  Probando Estadísticas...")
    try:
        response = requests.get(f'{BASE_URL}/api/statistics', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Estadísticas: Top 3 = [{data.get('top1')}, {data.get('top2')}, {data.get('top3')}]")
            return True
        else:
            print(f"   ❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

# Ejecutar todas las pruebas
if __name__ == '__main__':
    results = []
    
    # Health check
    results.append(test_health())
    
    # Registro
    results.append(test_register())
    
    # Login
    user_id = test_login()
    results.append(user_id is not None)
    
    # Sorteo
    numbers = test_sorteo()
    results.append(numbers is not None)
    
    # Guardar sorteo
    if user_id and numbers:
        results.append(test_save_sorteo(user_id, numbers))
        results.append(test_history(user_id))
    else:
        results.append(False)
        results.append(False)
    
    # Estadísticas
    results.append(test_statistics())
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Exitosas: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron! Tu backend está funcionando perfectamente.")
    else:
        print(f"\n⚠️  {total - passed} prueba(s) fallaron. Revisa los errores arriba.")
    
    print("="*60 + "\n")
    
    sys.exit(0 if passed == total else 1)
