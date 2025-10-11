# 🚀 Guía Rápida - Empezar a Desarrollar

## Estado Actual

### ✅ Lo que Funciona
- Backend API con FastAPI (http://localhost:8000)
- Base de datos SQLite configurada
- Sistema de archivos para uploads
- Documentación Swagger (/docs)

### ⏳ Lo que Falta
- Autenticación de usuarios
- CRUD de expedientes
- Subida de archivos
- Frontend React
- Sistema de permisos

---

## 🎯 Empezar en 3 Pasos

### Paso 1: Iniciar Backend

```bash
cd backend
./start.sh          # Linux/Mac
# o start.bat       # Windows
```

Verás:
```
🚀 Iniciando PanamaHealth Vault API...
📁 Directorio de uploads: /path/to/backend/uploads
💾 Base de datos: sqlite:///path/to/backend/panamahealth.db
✅ Base de datos inicializada correctamente
✅ API lista en http://localhost:8000
📚 Documentación en http://localhost:8000/docs
```

### Paso 2: Ver la API

Abre: http://localhost:8000

Deberías ver:
```json
{
  "message": "PanamaHealth Vault API",
  "status": "online",
  "version": "1.0.0",
  "mode": "local",
  "database": "SQLite",
  "docs": "/docs"
}
```

### Paso 3: Explorar Swagger

Abre: http://localhost:8000/docs

Verás la documentación interactiva (aunque aún no hay endpoints implementados).

---

## 📝 Próximos Pasos de Desarrollo

### 1. Implementar Autenticación (2-3 días)

**Archivos a crear:**

```
backend/app/models/user.py          - Modelo de usuario
backend/app/schemas/user.py         - Schemas Pydantic
backend/app/routers/auth.py         - Endpoints de auth
backend/app/services/auth_service.py - Lógica de autenticación
backend/app/utils/security.py       - Funciones de seguridad
```

**Endpoints a implementar:**
```python
POST /api/auth/register  - Registro
POST /api/auth/login     - Login
GET  /api/auth/me        - Usuario actual
```

### 2. Implementar Expedientes (3-4 días)

**Archivos a crear:**

```
backend/app/models/medical_record.py
backend/app/schemas/record.py
backend/app/routers/records.py
backend/app/services/record_service.py
backend/app/utils/file_handler.py
```

**Endpoints a implementar:**
```python
POST   /api/records         - Crear expediente
GET    /api/records         - Listar expedientes
GET    /api/records/{id}    - Ver expediente
PUT    /api/records/{id}    - Actualizar
DELETE /api/records/{id}    - Eliminar
POST   /api/records/{id}/upload - Subir archivo
```

### 3. Sistema de Permisos (1-2 días)

**Archivos a crear:**

```
backend/app/models/permission.py
backend/app/schemas/permission.py
backend/app/routers/permissions.py
backend/app/services/permission_service.py
```

**Endpoints a implementar:**
```python
POST   /api/permissions           - Dar acceso
GET    /api/permissions           - Ver permisos
DELETE /api/permissions/{id}      - Revocar acceso
```

### 4. Frontend Básico (1 semana)

**Componentes a crear:**

```
frontend/src/pages/Login.tsx
frontend/src/pages/Register.tsx
frontend/src/pages/PatientDashboard.tsx
frontend/src/pages/DoctorDashboard.tsx
frontend/src/components/RecordCard.tsx
frontend/src/components/UploadModal.tsx
frontend/src/services/api.ts
```

---

## 🛠️ Comandos Útiles

### Backend

```bash
# Activar entorno virtual
cd backend
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Iniciar servidor
python -m app.main

# Crear nueva migración de DB (cuando agregues modelos)
alembic revision -m "descripcion"
alembic upgrade head

# Reset base de datos
rm panamahealth.db
python -m app.main  # Se recrea automáticamente
```

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar desarrollo
npm start

# Build para producción
npm run build
```

---

## 📖 Ejemplo: Implementar Login

### 1. Crear modelo de usuario

`backend/app/models/user.py`:
```python
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from ..database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # patient, doctor, admin
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 2. Crear schemas

`backend/app/schemas/user.py`:
```python
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True
```

### 3. Crear router

`backend/app/routers/auth.py`:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.user import UserRegister, UserLogin, UserResponse
from ..services import auth_service

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user: UserRegister, db: Session = Depends(get_db)):
    return auth_service.create_user(db, user)

@router.post("/login")
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    return auth_service.authenticate_user(db, credentials)
```

### 4. Incluir en main.py

```python
from app.routers import auth

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
```

---

## 🎯 Checklist de Desarrollo

### Semana 1: Autenticación
- [ ] Modelo User
- [ ] Schemas de autenticación
- [ ] Router de auth
- [ ] Service de auth
- [ ] Funciones de seguridad (hash, JWT)
- [ ] Tests básicos

### Semana 2: Expedientes
- [ ] Modelo MedicalRecord
- [ ] Schemas de expedientes
- [ ] Router de records
- [ ] Service de records
- [ ] Subida de archivos
- [ ] Tests

### Semana 3: Permisos
- [ ] Modelo Permission
- [ ] Sistema de permisos
- [ ] Middleware de autorización
- [ ] Logs de auditoría

### Semana 4: Frontend
- [ ] Setup React
- [ ] Páginas de auth
- [ ] Dashboard básico
- [ ] Integración con API

---

## 💡 Tips

1. **Usa Swagger** - http://localhost:8000/docs para probar tus endpoints
2. **SQLite Browser** - Descarga DB Browser for SQLite para ver la DB
3. **Hot Reload** - FastAPI recarga automáticamente al cambiar código
4. **Logs** - Usa `print()` o `logging` para debug
5. **Postman** - Útil para probar la API

---

## 📚 Recursos

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [React Docs](https://react.dev/)
- [JWT.io](https://jwt.io/) - Decodificar tokens

---

## 🆘 Ayuda

Si tienes dudas:
1. Lee [ARCHITECTURE.md](../ARCHITECTURE.md)
2. Revisa [docs/TECH_STACK.md](../docs/TECH_STACK.md)
3. Crea un issue en GitHub
4. Email: info@panamahealth-vault.com

---

**¡Empieza a desarrollar!** 🚀

Samsung Innovation Campus 2025

