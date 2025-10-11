@echo off
REM Script para iniciar el backend localmente en Windows

echo ======================================
echo 🏥 PanamaHealth Vault - Backend Local
echo ======================================

REM Verificar si existe el entorno virtual
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo 📥 Instalando dependencias...
pip install -r requirements.txt

REM Iniciar servidor
echo 🚀 Iniciando servidor...
echo ✅ API: http://localhost:8000
echo 📚 Docs: http://localhost:8000/docs
echo ======================================
python -m app.main

pause

