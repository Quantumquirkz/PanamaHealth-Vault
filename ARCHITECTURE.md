# 🏗️ Arquitectura del Sistema

## Visión General

PanamaHealth Vault utiliza una arquitectura simple de 2 capas **SIN DOCKER**:

1. **Frontend** - Interfaz web con React (localhost:3000)
2. **Backend** - API REST con FastAPI (localhost:8000)
   - Base de datos: SQLite (archivo local)
   - Archivos: Sistema de archivos local

**NO REQUIERE:**
- ❌ Docker / Docker Compose
- ❌ PostgreSQL
- ❌ Redis
- ❌ MinIO/S3
- ❌ Ningún contenedor

---

## Diagrama de Arquitectura (Local)

```
┌──────────────────────────────────────────┐
│         FRONTEND (React)                 │
│      http://localhost:3000               │
│                                          │
│  ┌────────────┐    ┌──────────────┐    │
│  │  Portal    │    │  Dashboard   │    │
│  │ Pacientes  │    │   Médicos    │    │
│  └────────────┘    └──────────────┘    │
│                                          │
│  React + TypeScript + Tailwind CSS      │
└──────────────────────────────────────────┘
                    │
                    │ HTTP/REST (JWT)
                    │
┌──────────────────────────────────────────┐
│       BACKEND API (FastAPI)              │
│      http://localhost:8000               │
│                                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │  Auth   │  │ Records │  │   OCR   │ │
│  │ Module  │  │  Module │  │ Module  │ │
│  └─────────┘  └─────────┘  └─────────┘ │
│                                          │
│  FastAPI + SQLAlchemy                   │
└──────────────────────────────────────────┘
                    │
                    │
┌──────────────────────────────────────────┐
│    ALMACENAMIENTO LOCAL                  │
│                                          │
│  📁 backend/uploads/                     │
│     └── medical-records/                 │
│         ├── patient1_file1.pdf           │
│         ├── patient1_file2.jpg           │
│         └── ...                          │
│                                          │
│  💾 backend/panamahealth.db (SQLite)     │
│     ├── users                            │
│     ├── medical_records                  │
│     ├── access_permissions               │
│     └── audit_logs                       │
└──────────────────────────────────────────┘
```

---

## Componentes Detallados

### 1. Frontend (React)

**Responsabilidades:**
- Interfaz de usuario
- Manejo de estado con React Query
- Validación de formularios
- Visualización de documentos

**Estructura:**
```
frontend/
├── src/
│   ├── components/        # Componentes reutilizables
│   ├── pages/            # Páginas principales
│   │   ├── Login.tsx
│   │   ├── PatientDashboard.tsx
│   │   └── DoctorDashboard.tsx
│   ├── services/         # Llamadas a API
│   ├── hooks/            # Custom hooks
│   └── utils/            # Utilidades
└── public/
```

**Tecnologías:**
- React 18
- TypeScript
- React Router
- React Query (para estado del servidor)
- Tailwind CSS
- Axios (para llamadas HTTP)

---

### 2. Backend (FastAPI)

**Responsabilidades:**
- API REST
- Autenticación y autorización
- Lógica de negocio
- Procesamiento de archivos
- OCR de documentos

**Estructura:**
```
backend/
├── app/
│   ├── main.py           # Punto de entrada
│   ├── config.py         # Configuración
│   ├── models/           # Modelos de DB
│   │   ├── user.py
│   │   ├── record.py
│   │   └── permission.py
│   ├── schemas/          # Schemas Pydantic
│   ├── routers/          # Endpoints
│   │   ├── auth.py
│   │   ├── records.py
│   │   └── users.py
│   ├── services/         # Lógica de negocio
│   │   ├── auth_service.py
│   │   ├── record_service.py
│   │   └── ocr_service.py
│   └── utils/
│       ├── security.py
│       └── storage.py
└── tests/
```

**Endpoints Principales:**

```
POST   /api/auth/register     # Registro de usuario
POST   /api/auth/login        # Login
GET    /api/users/me          # Usuario actual

POST   /api/records           # Crear expediente
GET    /api/records           # Listar expedientes
GET    /api/records/{id}      # Ver expediente
DELETE /api/records/{id}      # Eliminar expediente

POST   /api/permissions       # Dar acceso a médico
GET    /api/permissions       # Ver permisos
DELETE /api/permissions/{id}  # Revocar acceso
```

---

### 3. Almacenamiento Local

#### Base de Datos (SQLite)

**Archivo**: `backend/panamahealth.db` (SQLite)

**Esquema de Base de Datos:**

```sql
-- Usuarios
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('patient', 'doctor', 'admin')),
    cedula VARCHAR(20) UNIQUE,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Expedientes médicos
CREATE TABLE medical_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50), -- 'exam', 'prescription', 'diagnosis', 'other'
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(50),
    file_size INTEGER,
    ocr_text TEXT,
    ocr_processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Permisos de acceso
CREATE TABLE access_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    doctor_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revoked_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(patient_id, doctor_id)
);

-- Logs de auditoría
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    record_id UUID REFERENCES medical_records(id),
    action VARCHAR(50) NOT NULL, -- 'view', 'create', 'update', 'delete'
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance
CREATE INDEX idx_records_patient ON medical_records(patient_id);
CREATE INDEX idx_permissions_patient ON access_permissions(patient_id);
CREATE INDEX idx_permissions_doctor ON access_permissions(doctor_id);
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_record ON audit_logs(record_id);
```

#### Almacenamiento de Archivos (Local)

```
backend/uploads/
└── medical-records/
    ├── {uuid}_documento1.pdf
    ├── {uuid}_examen1.jpg
    └── ...

Estructura:
- Carpeta base: backend/uploads/
- Subcarpeta: medical-records/
- Nombres: {UUID}_{nombre_original}.{extensión}
- Tamaño máximo: 10MB por archivo
- Formatos permitidos: PDF, JPG, PNG
```

---

## Flujos de Trabajo

### Flujo 1: Registro e Inicio de Sesión

```
1. Usuario ingresa datos en formulario
2. Frontend valida datos
3. Frontend envía POST /api/auth/register
4. Backend valida y hashea contraseña
5. Backend crea usuario en DB
6. Backend genera token JWT
7. Frontend guarda token y redirige a dashboard
```

### Flujo 2: Subir Documento Médico

```
1. Paciente selecciona archivo PDF/imagen
2. Frontend valida tipo y tamaño
3. Frontend envía POST /api/records con multipart/form-data
4. Backend valida autenticación
5. Backend sube archivo a MinIO
6. Backend crea registro en DB
7. Backend encola trabajo de OCR (background)
8. OCR procesa documento y actualiza DB
9. Frontend muestra confirmación
```

### Flujo 3: Médico Accede a Expediente

```
1. Médico busca paciente por nombre/cédula
2. Frontend envía GET /api/records?patient_id=X
3. Backend verifica permiso en access_permissions
4. Si tiene permiso, devuelve lista de expedientes
5. Médico selecciona documento
6. Frontend visualiza PDF/imagen
7. Backend registra acceso en audit_logs
```

### Flujo 4: Compartir Expediente con Médico

```
1. Paciente busca médico
2. Paciente selecciona médico y otorga acceso
3. Frontend envía POST /api/permissions
4. Backend crea registro en access_permissions
5. Backend envía notificación (futuro)
6. Médico ahora puede ver expedientes
```

---

## Seguridad

### Autenticación

```python
# JWT con access token
# Expiración: 24 horas
# Algoritmo: HS256

# Ejemplo de payload:
{
    "sub": "user_id",
    "email": "user@email.com",
    "role": "patient",
    "exp": 1234567890
}
```

### Autorización

```python
# Decorador para proteger endpoints
@router.get("/records/{record_id}")
async def get_record(
    record_id: UUID,
    current_user: User = Depends(get_current_user)
):
    # Verificar que el usuario tenga permiso
    if not has_access(current_user, record_id):
        raise HTTPException(status_code=403)
    return record
```

### Almacenamiento de Archivos

- Archivos guardados en MinIO con nombres UUID
- Encriptación en tránsito (HTTPS)
- Control de acceso por usuario
- Límite de tamaño: 10MB por archivo

---

## Escalabilidad

### Fase Actual (MVP)
- 1 instancia de backend
- 1 base de datos PostgreSQL
- 1 instancia de MinIO
- Soporta ~100 usuarios concurrentes

### Fase 2 (Crecimiento)
- Load balancer + múltiples instancias backend
- PostgreSQL con réplicas de lectura
- Redis para caché
- CDN para archivos estáticos
- Soporta ~10,000 usuarios

### Fase 3 (Producción)
- Kubernetes para orquestación
- PostgreSQL con sharding
- MinIO distribuido
- Múltiples regiones
- Soporta ~100,000+ usuarios

---

## Monitoreo

### Métricas Clave

- **Disponibilidad**: Uptime del sistema
- **Latencia**: Tiempo de respuesta de API
- **Throughput**: Requests por segundo
- **Errores**: Tasa de errores 4xx/5xx
- **Storage**: Espacio usado en MinIO

### Herramientas

- **Logs**: Python logging + archivo
- **Métricas**: Endpoint /metrics (futuro)
- **Alertas**: Email en errores críticos
- **Backups**: PostgreSQL diario, MinIO semanal

---

## Testing

### Backend
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Coverage
pytest --cov=app tests/
```

### Frontend
```bash
# Component tests
npm run test

# E2E tests
npm run test:e2e
```

---

## Despliegue

### Desarrollo Local (SIN DOCKER)
```bash
# Backend
cd backend && ./start.sh

# Frontend (otra terminal)
cd frontend && npm install && npm start
```

### Producción (ejemplo con Railway/Render)
```bash
# Backend: Deploy directo con Python
# Frontend: Deploy con build de React
# DB: SQLite o migrar a PostgreSQL
# Storage: Sistema de archivos o S3

# NO SE REQUIERE Docker en ningún momento
```

---

## Variables de Entorno

```env
# Backend
DATABASE_URL=postgresql://user:pass@localhost/dbname
SECRET_KEY=your-secret-key-here
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
REDIS_URL=redis://localhost:6379

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

---

## Próximas Mejoras Técnicas

1. **Caché**: Implementar Redis para sesiones y queries frecuentes
2. **CDN**: Servir archivos estáticos desde CDN
3. **Queue**: Celery para procesamiento asíncrono de OCR
4. **Search**: Elasticsearch para búsqueda full-text
5. **Real-time**: WebSockets para notificaciones en vivo

---

<div align="center">

**Arquitectura simple, escalable y mantenible**

*Samsung Innovation Campus 2025*

</div>
