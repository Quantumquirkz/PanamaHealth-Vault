#!/bin/bash

# Script para iniciar el backend localmente
echo "======================================"
echo "🏥 PanamaHealth Vault - Backend Local"
echo "======================================"

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Iniciar servidor
echo "🚀 Iniciando servidor..."
echo "✅ API: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
echo "======================================"
python -m app.main

