# Script de inicio rápido para Windows

Write-Host "🚀 Iniciando Sorteo Lotería API..." -ForegroundColor Green
Write-Host ""

# Verificar si existe el entorno virtual
if (-Not (Test-Path "venv")) {
    Write-Host "📦 Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
}

# Activar entorno virtual
Write-Host "🔌 Activando entorno virtual..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Instalar dependencias
Write-Host "📥 Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt

# Iniciar servidor
Write-Host ""
Write-Host "✅ Servidor listo en http://localhost:8080" -ForegroundColor Green
Write-Host ""
python app.py
