#!/bin/bash

echo "🚀 Preparando Backend para Render..."
echo ""

# Navegar a la carpeta backend
cd backend || exit

echo "✅ Verificando archivos necesarios..."
files=("requirements.txt" "Procfile" "runtime.txt" "wsgi.py" "app.py" "database.py")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ Falta: $file"
        exit 1
    fi
done

echo ""
echo "✅ Todos los archivos necesarios están presentes"
echo ""

# Inicializar git si no existe
if [ ! -d .git ]; then
    echo "📦 Inicializando repositorio Git..."
    git init
    git branch -M main
fi

echo ""
echo "📝 Agregando archivos al repositorio..."
git add .

echo ""
echo "💾 Haciendo commit..."
git commit -m "Backend Sorteo Lotería - Listo para Render"

echo ""
echo "✅ ¡Listo para subir a GitHub!"
echo ""
echo "🔗 Próximos pasos:"
echo "1. Crea un repositorio en GitHub: https://github.com/new"
echo "2. Nombre sugerido: sorteo-loteria-backend"
echo "3. Ejecuta estos comandos:"
echo ""
echo "   git remote add origin https://github.com/TU_USUARIO/sorteo-loteria-backend.git"
echo "   git push -u origin main"
echo ""
echo "4. Luego ve a Render: https://dashboard.render.com/"
echo ""
