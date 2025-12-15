# 🧪 Scripts de Prueba para la API

## 🏠 Probar Localmente

### Iniciar el servidor:
```powershell
cd backend
python app.py
```

### Probar Health Check:
```powershell
curl http://localhost:8080/health
```

### Probar Info de la API:
```powershell
curl http://localhost:8080/
```

---

## 🔐 Probar Autenticación

### Registrar un usuario:
```powershell
curl -X POST http://localhost:8080/api/register `
  -H "Content-Type: application/json" `
  -d '{\"username\": \"test\", \"password\": \"123456\"}'
```

### Login:
```powershell
curl -X POST http://localhost:8080/api/login `
  -H "Content-Type: application/json" `
  -d '{\"username\": \"test\", \"password\": \"123456\"}'
```

Respuesta (guarda el `user_id`):
```json
{
  "success": true,
  "user_id": 1,
  "message": "Login exitoso"
}
```

---

## 🎲 Probar Sorteos

### Generar sorteo:
```powershell
curl http://localhost:8080/api/sorteo
```

Respuesta:
```json
{
  "balotas": [12, 23, 5, 34, 18, 9]
}
```

### Guardar sorteo:
```powershell
curl -X POST http://localhost:8080/api/save_sorteo `
  -H "Content-Type: application/json" `
  -d '{\"user_id\": 1, \"numbers\": [12, 23, 5, 34, 18, 9]}'
```

### Ver historial (user_id = 1):
```powershell
curl http://localhost:8080/api/history/1
```

### Obtener estadísticas:
```powershell
curl http://localhost:8080/api/statistics
```

---

## 📊 Probar con Render (Después del Deploy)

Reemplaza `localhost:8080` con tu URL de Render:

### Health Check:
```powershell
curl https://tu-app.onrender.com/health
```

### Generar sorteo:
```powershell
curl https://tu-app.onrender.com/api/sorteo
```

### Registrar usuario:
```powershell
curl -X POST https://tu-app.onrender.com/api/register `
  -H "Content-Type: application/json" `
  -d '{\"username\": \"test\", \"password\": \"123456\"}'
```

### Login:
```powershell
curl -X POST https://tu-app.onrender.com/api/login `
  -H "Content-Type: application/json" `
  -d '{\"username\": \"test\", \"password\": \"123456\"}'
```

---

## 🗑️ Probar CRUD de Sorteos

### Eliminar sorteo (ID = 1):
```powershell
curl -X DELETE http://localhost:8080/api/sorteo/1
```

### Actualizar sorteo (ID = 1):
```powershell
curl -X PUT http://localhost:8080/api/sorteo/1 `
  -H "Content-Type: application/json" `
  -d '{\"numbers\": [5, 10, 15, 20, 25, 7]}'
```

---

## 📤 Probar Upload de Excel

```powershell
curl -X POST http://localhost:8080/api/upload `
  -F "file=@ruta/al/archivo.xlsx"
```

---

## 🧪 Script de Prueba Completo

Guarda esto como `test_api.ps1`:

```powershell
# Script de prueba completa de la API
$BASE_URL = "http://localhost:8080"

Write-Host "🧪 Testing Sorteo Lotería API" -ForegroundColor Green
Write-Host ""

# 1. Health Check
Write-Host "1️⃣ Health Check..." -ForegroundColor Yellow
curl "$BASE_URL/health"
Write-Host ""

# 2. API Info
Write-Host "2️⃣ API Info..." -ForegroundColor Yellow
curl "$BASE_URL/"
Write-Host ""

# 3. Register
Write-Host "3️⃣ Registrando usuario..." -ForegroundColor Yellow
$register = curl -X POST "$BASE_URL/api/register" `
  -H "Content-Type: application/json" `
  -d '{\"username\": \"testuser\", \"password\": \"123456\"}' | ConvertFrom-Json
Write-Host $register
Write-Host ""

# 4. Login
Write-Host "4️⃣ Login..." -ForegroundColor Yellow
$login = curl -X POST "$BASE_URL/api/login" `
  -H "Content-Type: application/json" `
  -d '{\"username\": \"testuser\", \"password\": \"123456\"}' | ConvertFrom-Json
$userId = $login.user_id
Write-Host "User ID: $userId"
Write-Host ""

# 5. Generate Sorteo
Write-Host "5️⃣ Generando sorteo..." -ForegroundColor Yellow
$sorteo = curl "$BASE_URL/api/sorteo" | ConvertFrom-Json
$numbers = $sorteo.balotas
Write-Host "Balotas: $numbers"
Write-Host ""

# 6. Save Sorteo
Write-Host "6️⃣ Guardando sorteo..." -ForegroundColor Yellow
curl -X POST "$BASE_URL/api/save_sorteo" `
  -H "Content-Type: application/json" `
  -d "{\"user_id\": $userId, \"numbers\": $numbers}"
Write-Host ""

# 7. Get History
Write-Host "7️⃣ Obteniendo historial..." -ForegroundColor Yellow
curl "$BASE_URL/api/history/$userId"
Write-Host ""

# 8. Get Statistics
Write-Host "8️⃣ Obteniendo estadísticas..." -ForegroundColor Yellow
curl "$BASE_URL/api/statistics"
Write-Host ""

Write-Host "✅ Todas las pruebas completadas!" -ForegroundColor Green
```

### Ejecutar el script:
```powershell
.\test_api.ps1
```

---

## 📋 Respuestas Esperadas

### ✅ Health Check:
```json
{
  "status": "healthy",
  "message": "Sorteo Lotería API is running"
}
```

### ✅ Sorteo Generado:
```json
{
  "balotas": [12, 23, 5, 34, 18, 9]
}
```

### ✅ Login Exitoso:
```json
{
  "success": true,
  "user_id": 1,
  "message": "Login exitoso"
}
```

### ✅ Historial:
```json
{
  "history": [
    {
      "id": 1,
      "numbers": [12, 23, 5, 34, 18, 9],
      "date": "2025-12-06 10:30:00"
    }
  ]
}
```

---

## 🔧 Troubleshooting

### Error de conexión:
```
Error: Connection refused
```
**Solución:** Asegúrate de que el servidor esté corriendo:
```bash
python backend/app.py
```

### Error 404:
```
Error: 404 Not Found
```
**Solución:** Verifica la URL del endpoint

### Error 500:
```
Error: 500 Internal Server Error
```
**Solución:** Revisa los logs del servidor

---

**¡Prueba todos los endpoints antes de deployar! 🚀**
