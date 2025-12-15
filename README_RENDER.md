# 🚀 Guía de Despliegue en Render

## 📋 Pasos para Desplegar en Render

### 1. Preparar el Repositorio

Asegúrate de que tu código esté en GitHub:

```bash
cd backend
git init
git add .
git commit -m "Initial commit - Backend for Render"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/sorteo-loteria-backend.git
git push -u origin main
```

### 2. Crear Web Service en Render

1. Ve a [Render Dashboard](https://dashboard.render.com/)
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Configura el servicio:

#### Configuración Básica:
- **Name**: `sorteo-loteria-api`
- **Region**: Elige la más cercana (ej: Oregon - USA)
- **Branch**: `main`
- **Root Directory**: `backend` (si el backend está en una subcarpeta)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

#### Variables de Entorno:
Añade estas variables en la sección **Environment**:
- `FLASK_ENV` = `production`
- `PYTHON_VERSION` = `3.11.0`

### 3. Desplegar

1. Click en **"Create Web Service"**
2. Render automáticamente:
   - Instalará las dependencias
   - Iniciará tu aplicación
   - Te dará una URL pública (ej: `https://sorteo-loteria-api.onrender.com`)

### 4. Verificar el Despliegue

Una vez desplegado, prueba tu API:

```bash
curl https://tu-app.onrender.com/health
```

Deberías recibir:
```json
{
  "status": "healthy",
  "message": "Sorteo Lotería API is running"
}
```

### 5. Probar el Endpoint de Sorteo

```bash
curl https://tu-app.onrender.com/api/sorteo
```

Respuesta esperada:
```json
{
  "balotas": [12, 23, 34, 5, 18, 9]
}
```

---

## 📱 Conectar Flutter con la API

Actualiza la URL en tu app Flutter:

### `lib/lottery_service.dart`:
```dart
class LotteryService {
  static const String baseUrl = 'https://tu-app.onrender.com';
  // ...
}
```

### `lib/auth_service.dart`:
```dart
class AuthService {
  static const String baseUrl = 'https://tu-app.onrender.com';
  // ...
}
```

---

## 🔧 Solución de Problemas

### Error: "Application failed to respond"
- Verifica que el comando de inicio sea correcto
- Revisa los logs en Render Dashboard

### Error: "Build failed"
- Verifica que `requirements.txt` esté correcto
- Asegúrate de que todas las dependencias sean compatibles

### Base de datos se resetea
- Render usa almacenamiento efímero en el plan gratuito
- Considera usar un servicio de base de datos persistente (PostgreSQL en Render)

### CORS errors
- Verifica que `CORS_ORIGINS = "*"` esté configurado en `config.py`
- Esto permite peticiones desde cualquier origen

---

## 📊 Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/register` | Registrar usuario |
| POST | `/api/login` | Iniciar sesión |
| GET | `/api/sorteo` | Generar sorteo |
| POST | `/api/save_sorteo` | Guardar sorteo |
| GET | `/api/history/<user_id>` | Obtener historial |
| GET | `/api/statistics` | Obtener estadísticas |
| POST | `/api/upload` | Subir Excel |
| DELETE | `/api/sorteo/<id>` | Eliminar sorteo |
| PUT | `/api/sorteo/<id>` | Actualizar sorteo |

---

## 💰 Plan Gratuito de Render

### Límites:
- ✅ 750 horas/mes de runtime gratuito
- ✅ Aplicaciones se suspenden después de 15 min de inactividad
- ✅ Arranque puede tomar ~30 segundos
- ⚠️ Almacenamiento efímero (la DB se resetea)

### Recomendaciones:
- Para producción real, considera el plan pagado ($7/mes)
- Usa PostgreSQL para persistencia de datos
- Configura health checks automáticos

---

## 🎯 Próximos Pasos

1. ✅ Desplegar en Render
2. 🔄 Actualizar URLs en Flutter
3. 🧪 Probar todos los endpoints
4. 📊 Monitorear logs en Render
5. 🚀 ¡Compartir tu app!

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Render Dashboard
2. Verifica las variables de entorno
3. Confirma que el puerto esté correcto (`$PORT`)
4. Asegúrate de que `gunicorn` esté en `requirements.txt`
