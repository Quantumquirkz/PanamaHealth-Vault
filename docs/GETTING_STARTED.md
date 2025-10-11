# 🚀 Guía de Inicio Rápido (SIN DOCKER)

Esta guía te ayudará a configurar el proyecto **completamente en local, SIN DOCKER ni servicios externos** en menos de 5 minutos.

---

## 🎯 Importante: NO SE REQUIERE DOCKER

Este proyecto funciona **100% sin Docker**. Solo necesitas Python y Node.js.

## Prerrequisitos

**Solo necesitas 3 cosas:**

- ✅ **Python 3.11+** - [Descargar aquí](https://www.python.org/downloads/)
- ✅ **Node.js 18+** - [Descargar aquí](https://nodejs.org/)
- ✅ **Git** - [Descargar aquí](https://git-scm.com/)

**NO NECESITAS:**
- ❌ Docker
- ❌ Docker Compose  
- ❌ PostgreSQL
- ❌ Redis
- ❌ MinIO
- ❌ Ningún servicio externo

### Verificar instalaciones

```bash
python --version   # o python3 --version
node --version
npm --version
git --version
```

---

## 🎯 Instalación en 3 Pasos

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/quantumquirkz/PanamaHealth-Vault.git
cd PanamaHealth-Vault
```

### Paso 2: Iniciar Backend (Terminal 1)

#### Linux/Mac:
```bash
cd backend
chmod +x start.sh
./start.sh
```

#### Windows:
```cmd
cd backend
start.bat
```

#### Manual (alternativo):
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```

**El backend estará en:** http://localhost:8000

### Paso 3: Iniciar Frontend (Terminal 2)

```bash
cd frontend
npm install
npm start
```

**El frontend estará en:** http://localhost:3000

---

## ✅ Verificar Instalación

### 1. Verificar Backend

Abre tu navegador en: http://localhost:8000

Deberías ver:
```json
{
  "message": "PanamaHealth Vault API",
  "status": "online",
  "version": "1.0.0",
  "mode": "local",
  "database": "SQLite"
}
```

### 2. Verificar Documentación API

Abre: http://localhost:8000/docs

Verás la documentación interactiva de Swagger.

### 3. Verificar Base de Datos

```bash
# Desde la carpeta backend
ls -la panamahealth.db  # Linux/Mac
dir panamahealth.db     # Windows
```

Deberías ver el archivo `panamahealth.db` creado automáticamente.

### 4. Verificar Carpeta de Uploads

```bash
# Desde la carpeta backend
ls -la uploads/         # Linux/Mac
dir uploads\            # Windows
```

Debería existir la carpeta `uploads/medical-records/`.

---

## 📁 Estructura Creada Automáticamente

```
PanamaHealth-Vault/
├── backend/
│   ├── panamahealth.db           # ✅ Base de datos SQLite (auto-creado)
│   ├── uploads/                  # ✅ Archivos médicos (auto-creado)
│   │   └── medical-records/
│   ├── venv/                     # ✅ Entorno virtual Python
│   └── app/
└── frontend/
    └── node_modules/             # ✅ Dependencias Node
```

---

## 🔧 Configuración (Opcional)

### Cambiar Puerto del Backend

Edita `backend/app/main.py`:

```python
# Línea final
uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)  # Cambiar 8000 a 8080
```

### Habilitar OCR (Opcional)

1. Instalar Tesseract:

```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-spa

# macOS
brew install tesseract tesseract-lang

# Windows - Descargar de:
# https://github.com/UB-Mannheim/tesseract/wiki
```

2. Descomentar en `requirements.txt`:

```txt
# Descomentar estas líneas:
pytesseract==0.3.10
pdf2image==1.16.3
```

3. Habilitar en `backend/app/config.py`:

```python
OCR_ENABLED: bool = True
```

---

## 🛠️ Comandos Útiles

### Backend

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar nueva dependencia
pip install nombre-paquete
pip freeze > requirements.txt

# Desactivar entorno virtual
deactivate

# Eliminar base de datos (reset)
rm panamahealth.db  # Linux/Mac
del panamahealth.db # Windows
```

### Frontend

```bash
# Instalar nueva dependencia
npm install nombre-paquete

# Limpiar caché
npm cache clean --force

# Reinstalar todo
rm -rf node_modules package-lock.json
npm install
```

---

## 🐛 Problemas Comunes

### Error: "Puerto ya en uso"

```bash
# Matar proceso en puerto 8000
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Error: "Python no encontrado"

```bash
# Probar con python3
python3 --version
python3 -m venv venv
```

### Error: "Module not found"

```bash
# Reinstalar dependencias
cd backend
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "Cannot find module"

```bash
# Frontend - reinstalar
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Base de datos corrupta

```bash
# Eliminar y recrear
cd backend
rm panamahealth.db
python -m app.main  # Se creará automáticamente
```

---

## 🎓 Próximos Pasos

Una vez que todo esté funcionando:

1. ✅ Explora la API: http://localhost:8000/docs
2. ✅ Prueba los endpoints en Swagger
3. ✅ Revisa [ARCHITECTURE.md](../ARCHITECTURE.md)
4. ✅ Lee [TECH_STACK.md](TECH_STACK.md)
5. ✅ Empieza a desarrollar

---

## 📊 Resumen de URLs

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Frontend** | http://localhost:3000 | Aplicación React |
| **Backend API** | http://localhost:8000 | API REST |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **ReDoc** | http://localhost:8000/redoc | Documentación alternativa |
| **Health Check** | http://localhost:8000/health | Estado del sistema |

---

## 🔒 Datos Almacenados

Todo se guarda localmente en tu máquina:

- **Base de datos**: `backend/panamahealth.db` (archivo SQLite)
- **Archivos médicos**: `backend/uploads/medical-records/`
- **Logs**: Consola (no se guarda en archivo)

### Backup

Para hacer backup de tus datos:

```bash
# Copiar base de datos
cp backend/panamahealth.db backup_$(date +%Y%m%d).db

# Copiar archivos
cp -r backend/uploads/ backup_uploads/
```

---

## 🧪 Testing (Opcional)

```bash
# Backend tests
cd backend
source venv/bin/activate
pytest

# Con cobertura
pytest --cov=app tests/

# Frontend tests
cd frontend
npm test
```

---

## 🚀 Desarrollo

### Crear nueva funcionalidad

1. **Backend**:
   - Agregar modelo en `backend/app/models/`
   - Crear schema en `backend/app/schemas/`
   - Implementar router en `backend/app/routers/`
   - Agregar servicio en `backend/app/services/`

2. **Frontend**:
   - Crear componente en `frontend/src/components/`
   - Agregar página en `frontend/src/pages/`
   - Implementar servicio API en `frontend/src/services/`

---

## 📞 Soporte

Si tienes problemas:

1. 📖 Revisa esta guía completa
2. 🔍 Busca en [GitHub Issues](https://github.com/quantumquirkz/PanamaHealth-Vault/issues)
3. 💬 Crea un nuevo issue
4. 📧 Email: info@panamahealth-vault.com

---

## 🎉 ¡Listo!

Ahora tienes el proyecto corriendo completamente en local, sin Docker ni AWS.

Todo simple, rápido y funcional. 🚀

---

**Samsung Innovation Campus 2025**
