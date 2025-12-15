# 🏗️ Backend Architecture - Flask with Blueprints

## 📁 Nueva Estructura del Proyecto

```
backend/
├── app.py                  # Aplicación principal (Application Factory)
├── config.py              # Configuración de la aplicación
├── database.py            # Utilidades de base de datos
├── requirements.txt       # Dependencias Python
├── Procfile              # Configuración para deployment
├── routes/               # Blueprints (módulos de rutas)
│   ├── __init__.py       # Inicialización del paquete
│   ├── auth.py           # Blueprint de autenticación
│   ├── lottery.py        # Blueprint de lotería
│   └── upload.py         # Blueprint de carga de archivos
└── lottery.db            # Base de datos SQLite (auto-generada)
```

---

## 🎯 Ventajas de esta Arquitectura

### ✅ Modularidad
- Cada blueprint maneja una funcionalidad específica
- Fácil de mantener y escalar
- Código más organizado y legible

### ✅ Separación de Responsabilidades
- **app.py**: Factory pattern y configuración principal
- **config.py**: Configuración centralizada
- **database.py**: Gestión de base de datos
- **routes/**: Lógica de endpoints separada por dominio

### ✅ Escalabilidad
- Fácil agregar nuevos blueprints
- Cada módulo es independiente
- Testing más sencillo

---

## 📚 Blueprints Implementados

### 1. **Auth Blueprint** (`routes/auth.py`)
Maneja autenticación de usuarios

**Endpoints:**
- `POST /api/register` - Registrar nuevo usuario
- `POST /api/login` - Iniciar sesión

**Características:**
- Hash de contraseñas con Werkzeug
- Validación de datos
- Manejo de errores de integridad

---

### 2. **Lottery Blueprint** (`routes/lottery.py`)
Maneja generación y gestión de sorteos

**Endpoints:**
- `GET /api/sorteo` - Generar nuevo sorteo
- `POST /api/save_sorteo` - Guardar sorteo
- `GET /api/history/<user_id>` - Obtener historial
- `GET /api/statistics` - Obtener estadísticas

**Características:**
- Algoritmo inteligente de generación
- Top 3 números más frecuentes
- Guardado en historial por usuario

---

### 3. **Upload Blueprint** (`routes/upload.py`)
Maneja carga y procesamiento de archivos Excel

**Endpoints:**
- `POST /api/upload` - Subir archivo Excel

**Características:**
- Validación de formato
- Procesamiento de datos con pandas
- Carga a base de datos SQLite
- Manejo de errores detallado

---

## 🔧 Archivo de Configuración

### `config.py`

Centraliza toda la configuración de la aplicación:

```python
class Config:
    SECRET_KEY = 'your-secret-key'
    DEBUG = False
    CORS_ORIGINS = ["http://localhost:*", ...]
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
```

**Ambientes:**
- `DevelopmentConfig` - Para desarrollo (DEBUG=True)
- `ProductionConfig` - Para producción (DEBUG=False)

---

## 🗄️ Database Module

### `database.py`

Gestiona conexiones y inicialización de la base de datos:

**Funciones:**
- `get_db_connection()` - Obtiene conexión a SQLite
- `init_db()` - Inicializa tablas
- `close_db_connection()` - Cierra conexión

**Características:**
- Row factory para acceso por nombre
- Path management automático
- Mensajes de éxito/error

---

## 🚀 Uso del Application Factory

### `app.py`

Usa el patrón Application Factory:

```python
def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app, ...)
    init_db()
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(lottery_bp)
    app.register_blueprint(upload_bp)
    
    return app
```

**Ventajas:**
- Fácil testing con diferentes configuraciones
- Múltiples instancias si es necesario
- Inicialización ordenada

---

## 🛠️ Cómo Ejecutar

### Desarrollo

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Con variables de entorno

```bash
# Windows PowerShell
$env:FLASK_ENV="production"
python app.py

# Linux/Mac
export FLASK_ENV=production
python app.py
```

---

## 📋 Endpoints Disponibles

### Health Check
```
GET /health
```
Respuesta:
```json
{
  "status": "healthy",
  "message": "Sorteo Lotería API is running"
}
```

### API Info
```
GET /
```
Respuesta:
```json
{
  "name": "Sorteo Lotería API",
  "version": "1.0.0",
  "endpoints": { ... }
}
```

---

## 🔐 Seguridad

### Implementada:
- ✅ Hash de contraseñas (Werkzeug)
- ✅ SQL parametrizado (previene SQLi)
- ✅ CORS configurado
- ✅ Validación de archivos
- ✅ Límite de tamaño de archivo

### Recomendaciones adicionales:
- [ ] JWT para autenticación stateless
- [ ] Rate limiting
- [ ] HTTPS en producción
- [ ] Variables de entorno para SECRET_KEY

---

## 📊 Flujo de Datos

```
Client Request
    ↓
Flask App (app.py)
    ↓
Blueprint Router
    ↓
Endpoint Handler
    ↓
Database Module (database.py)
    ↓
SQLite Database
    ↓
Response JSON
```

---

## 🧪 Testing

### Estructura sugerida:
```
backend/
└── tests/
    ├── __init__.py
    ├── test_auth.py
    ├── test_lottery.py
    └── test_upload.py
```

### Ejemplo de test:
```python
import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app('testing')
    yield app

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
```

---

## 🚀 Deployment

### Gunicorn (Producción)
```bash
gunicorn -w 4 -b :8080 "app:create_app('production')"
```

### Docker (Opcional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", ":8080", "app:create_app('production')"]
```

---

## 📝 Mejoras Futuras

- [ ] JWT Authentication
- [ ] Redis para caching
- [ ] Logging estructurado
- [ ] API versioning
- [ ] Swagger/OpenAPI docs
- [ ] Middleware para logging
- [ ] Error handlers personalizados
- [ ] Background tasks (Celery)

---

## 🎓 Patrones Aplicados

1. **Application Factory** - Creación flexible de app
2. **Blueprints** - Modularización de rutas
3. **Separation of Concerns** - Cada archivo una responsabilidad
4. **Configuration Management** - Configuración centralizada
5. **Database Connection Management** - Gestión de conexiones

---

¡La nueva arquitectura está lista y es más profesional, mantenible y escalable! 🎉
