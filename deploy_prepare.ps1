# Script de preparación para despliegue en Render
Write-Host "🚀 Preparando Backend para Render..." -ForegroundColor Cyan
Write-Host ""

# Navegar a la carpeta backend
Set-Location backend

Write-Host "✅ Verificando archivos necesarios..." -ForegroundColor Green
$files = @("requirements.txt", "Procfile", "runtime.txt", "wsgi.py", "app.py", "database.py")
$allPresent = $true

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Falta: $file" -ForegroundColor Red
        $allPresent = $false
    }
}

if (-not $allPresent) {
    Write-Host "`n❌ Faltan archivos necesarios. Abortando..." -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Todos los archivos necesarios están presentes" -ForegroundColor Green
Write-Host ""

# Verificar si git está instalado
try {
    git --version | Out-Null
} catch {
    Write-Host "❌ Git no está instalado. Instálalo desde: https://git-scm.com/" -ForegroundColor Red
    exit 1
}

# Inicializar git si no existe
if (-not (Test-Path .git)) {
    Write-Host "📦 Inicializando repositorio Git..." -ForegroundColor Yellow
    git init
    git branch -M main
}

Write-Host "📝 Agregando archivos al repositorio..." -ForegroundColor Yellow
git add .

Write-Host "`n💾 Haciendo commit..." -ForegroundColor Yellow
git commit -m "Backend Sorteo Lotería - Listo para Render"

Write-Host "`n✅ ¡Listo para subir a GitHub!" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 Próximos pasos:" -ForegroundColor Cyan
Write-Host "1. Crea un repositorio en GitHub: " -NoNewline
Write-Host "https://github.com/new" -ForegroundColor Blue
Write-Host "2. Nombre sugerido: " -NoNewline
Write-Host "sorteo-loteria-backend" -ForegroundColor Yellow
Write-Host "3. Ejecuta estos comandos:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   git remote add origin https://github.com/TU_USUARIO/sorteo-loteria-backend.git" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "4. Luego ve a Render: " -NoNewline
Write-Host "https://dashboard.render.com/" -ForegroundColor Blue
Write-Host ""

# Preguntar si quiere abrir los enlaces
$response = Read-Host "`n¿Quieres abrir GitHub en el navegador? (s/n)"
if ($response -eq 's' -or $response -eq 'S') {
    Start-Process "https://github.com/new"
}

$response = Read-Host "¿Quieres abrir Render Dashboard? (s/n)"
if ($response -eq 's' -or $response -eq 'S') {
    Start-Process "https://dashboard.render.com/"
}

Write-Host "`n🎉 ¡Éxito! Sigue las instrucciones arriba." -ForegroundColor Green
