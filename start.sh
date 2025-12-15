#!/bin/bash
# Script de inicio rápido para desarrollo local

echo "🚀 Iniciando Sorteo Lotería API..."
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python -m venv venv
fi

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Iniciar servidor
echo ""
echo "✅ Servidor listo en http://localhost:8080"
echo ""
python app.py
