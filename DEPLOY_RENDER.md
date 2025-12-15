# 🎯 Despliegue Rápido en Render - Sorteo Lotería

## ✅ Todo Listo para Desplegar

Tu backend está completamente preparado para Render. Sigue estos pasos:

---

## 📋 PASO 1: Subir a GitHub

```powershell
# Desde la carpeta backend
cd backend

# Inicializar Git (si no está inicializado)
git init

# Agregar todos los archivos
git add .

# Commit
git commit -m "Backend listo para Render"

# Crear repositorio en GitHub y conectar
git branch -M main
git remote add origin https://github.com/TU_USUARIO/sorteo-loteria-backend.git
git push -u origin main
```

---

## 📋 PASO 2: Crear Web Service en Render

### 2.1 Ir a Render
1. Visita: https://dashboard.render.com/
2. Login o Sign up (gratis)

### 2.2 Crear Nuevo Web Service
1. Click en **"New +"** (botón azul arriba a la derecha)
2. Selecciona **"Web Service"**

### 2.3 Conectar Repositorio
1. Conecta tu cuenta de GitHub
2. Busca tu repositorio: `sorteo-loteria-backend`
3. Click en **"Connect"**

### 2.4 Configurar el Servicio

**Información Básica:**
```
Name:           sorteo-loteria-api
Region:         Oregon (USA) o la más cercana
Branch:         main
Root Directory: (dejar vacío si backend está en la raíz, 
                 o poner "backend" si está en subcarpeta)
```

**Runtime:**
```
Environment:    Python 3
Python Version: 3.11.0
```

**Build & Deploy:**
```
Build Command:  pip install -r requirements.txt
Start Command:  gunicorn --workers 4 --bind 0.0.0.0:$PORT app:app
```

**Plan:**
```
Plan: Free (⚠️ se suspende tras 15min de inactividad)
```

### 2.5 Variables de Entorno

Click en **"Advanced"** y añade:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `PYTHON_VERSION` | `3.11.0` |

---

## 📋 PASO 3: Desplegar

1. Click en **"Create Web Service"**
2. Render comenzará a:
   - ✅ Clonar tu repositorio
   - ✅ Instalar Python 3.11
   - ✅ Instalar dependencias
   - ✅ Iniciar con Gunicorn
   - ✅ Asignar URL pública

**Tiempo estimado:** 3-5 minutos

---

## 📋 PASO 4: Verificar Despliegue

### 4.1 Obtener tu URL
Render te dará una URL como:
```
https://sorteo-loteria-api.onrender.com
```

### 4.2 Probar la API

**Health Check:**
```bash
curl https://TU-URL.onrender.com/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "message": "Sorteo Lotería API is running"
}
```

**Generar Sorteo:**
```bash
curl https://TU-URL.onrender.com/api/sorteo
```

**Respuesta esperada:**
```json
{
  "balotas": [12, 23, 5, 34, 18, 9]
}
```

---

## 📋 PASO 5: Conectar Flutter App

### 5.1 Actualizar URLs en Flutter

**Archivo: `lib/lottery_service.dart`**
```dart
class LotteryService {
  static const String baseUrl = 'https://TU-URL.onrender.com';
  // Resto del código...
}
```

**Archivo: `lib/auth_service.dart`**
```dart
class AuthService {
  static const String baseUrl = 'https://TU-URL.onrender.com';
  // Resto del código...
}
```

### 5.2 Probar la App

```bash
# En la raíz del proyecto Flutter
flutter run
```

---

## 🎉 ¡LISTO!

Tu API está desplegada y funcionando en:
```
https://TU-URL.onrender.com
```

### Endpoints Disponibles:

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | ✅ Health check |
| GET | `/` | 📄 Info de la API |
| POST | `/api/register` | 👤 Registrar usuario |
| POST | `/api/login` | 🔐 Login |
| GET | `/api/sorteo` | 🎲 Generar sorteo |
| POST | `/api/save_sorteo` | 💾 Guardar sorteo |
| GET | `/api/history/<id>` | 📜 Ver historial |
| GET | `/api/statistics` | 📊 Estadísticas |
| POST | `/api/upload` | 📤 Subir Excel |
| DELETE | `/api/sorteo/<id>` | 🗑️ Eliminar sorteo |
| PUT | `/api/sorteo/<id>` | ✏️ Editar sorteo |

---

## ⚠️ Notas Importantes

### Plan Gratuito de Render:
- ✅ **750 horas/mes** gratis
- ⚠️ **Se suspende** tras 15 min sin actividad
- ⏱️ **Tarda ~30seg** en despertar
- 💾 **Almacenamiento efímero** (la DB se resetea)

### Para Producción:
- Considera el plan pagado ($7/mes)
- Usa PostgreSQL para datos persistentes
- Configura custom domain

---

## 🔧 Troubleshooting

### ❌ Error: "Application failed to respond"
**Solución:**
- Verifica el Start Command
- Revisa los logs en Render Dashboard

### ❌ Error: "Build failed"
**Solución:**
- Verifica `requirements.txt`
- Asegura compatibilidad Python 3.11

### ❌ CORS errors en Flutter
**Solución:**
- Ya está configurado `CORS_ORIGINS = "*"` en `config.py`

### ❌ Base de datos vacía
**Solución:**
- El plan gratuito resetea la DB
- Usa PostgreSQL en Render (gratis 90 días)

---

## 📞 Soporte

**Logs en vivo:**
https://dashboard.render.com → Tu servicio → Logs

**Documentación Render:**
https://render.com/docs/deploy-flask

---

## 🚀 Siguientes Pasos

1. ✅ Desplegar en Render
2. 🔄 Actualizar URLs en Flutter
3. 🧪 Probar todos los endpoints
4. 📱 Instalar app en tu móvil
5. 🎉 ¡Compartir tu proyecto!

---

**¿Todo funcionando? ¡Felicidades! 🎉**

Tu app de lotería está en la nube y lista para usar.
