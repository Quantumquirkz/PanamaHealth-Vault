# 🏥 PanamaHealth Vault

## Sistema de Expedientes Médicos Digitales para Panamá

[![Estado](https://img.shields.io/badge/Estado-MVP-green.svg)](https://github.com/quantumquirkz/PanamaHealth-Vault)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-blue.svg)](LICENSE)

---

## 📋 Tabla de Contenidos

- [Visión General](#-visión-general)
- [Instalación](#-instalación-5-minutos)
- [Tecnologías](#-tecnologías)
- [Características](#-características)
- [Documentación](#-documentación)

---

## 🎯 Visión General

**PanamaHealth Vault** es una plataforma web que centraliza expedientes médicos digitales en Panamá, facilitando el acceso seguro a información de salud entre pacientes, médicos e instituciones.

### 🚫 SIN DOCKER - 100% Local

Este proyecto NO requiere Docker, PostgreSQL, Redis ni servicios externos. Todo funciona localmente con SQLite y el sistema de archivos.

### Objetivos del MVP

- ✅ Digitalizar y almacenar expedientes médicos
- ✅ Permitir acceso controlado entre pacientes y médicos
- ✅ Extraer información de documentos (OCR básico)
- ✅ Interfaz web simple y accesible

---

## 🚀 Instalación (5 minutos)

### Prerrequisitos

**Solo necesitas:**
- ✅ Python 3.11+
- ✅ Node.js 18+

**NO necesitas:**
- ❌ Docker
- ❌ PostgreSQL
- ❌ Redis
- ❌ AWS

### Instalación Rápida

```bash
# 1. Clonar repositorio
git clone https://github.com/quantumquirkz/PanamaHealth-Vault.git
cd PanamaHealth-Vault

# 2. Backend (Terminal 1)
cd backend
./start.sh          # Linux/Mac
# o start.bat       # Windows

# 3. Frontend (Terminal 2)
cd frontend
npm install
npm start
```

**¡Listo!**
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

Ver guía completa: [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)

---

## 🛠️ Tecnologías

### Backend
- **FastAPI** (Python 3.11+) - API REST
- **SQLite** - Base de datos local
- **SQLAlchemy** - ORM
- **JWT** - Autenticación

### Frontend
- **React** (TypeScript) - Interfaz web
- **Tailwind CSS** - Estilos
- **React Query** - Manejo de estado

### Almacenamiento
- **SQLite** - Base de datos en `backend/panamahealth.db`
- **Sistema de archivos** - Archivos en `backend/uploads/`

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────┐
│      FRONTEND (React)           │
│   http://localhost:3000         │
└────────────┬────────────────────┘
             │ HTTP/REST
┌────────────▼────────────────────┐
│    BACKEND API (FastAPI)        │
│   http://localhost:8000         │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│   ALMACENAMIENTO LOCAL          │
│  📁 uploads/                    │
│  💾 panamahealth.db (SQLite)    │
└─────────────────────────────────┘
```

Ver arquitectura completa: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## ⭐ Características

### MVP Actual

- [x] Backend API con FastAPI
- [x] Base de datos SQLite
- [x] Almacenamiento local de archivos
- [x] Estructura de proyecto completa
- [x] Configuración automática

### Próximamente

- [ ] Registro y autenticación de usuarios
- [ ] CRUD de expedientes médicos
- [ ] Subida de documentos
- [ ] Sistema de permisos
- [ ] OCR básico (opcional)
- [ ] Frontend React completo

---

## 📊 Base de Datos

### SQLite: `backend/panamahealth.db`

```
users                    - Pacientes y médicos
medical_records          - Expedientes médicos
access_permissions       - Control de acceso
audit_logs              - Registro de actividad
```

---

## 🔒 Seguridad

- **HTTPS** - Todas las comunicaciones
- **JWT** - Autenticación con tokens
- **RBAC** - Control de acceso por roles
- **Encriptación** - Archivos protegidos
- **Auditoría** - Logs de todos los accesos
- **Cumplimiento** - Ley 81 de 2019 (Panamá)

---

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| [GETTING_STARTED.md](docs/GETTING_STARTED.md) | Guía de instalación completa |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Arquitectura del sistema |
| [TECH_STACK.md](docs/TECH_STACK.md) | Stack tecnológico |

---

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'feat: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 🎯 Roadmap

### Fase 1: MVP (3 meses) - Actual
- ✅ Estructura del proyecto
- ✅ Backend base con FastAPI
- ✅ Base de datos SQLite
- 🔄 Autenticación y autorización
- 🔄 CRUD de expedientes

### Fase 2: Mejoras (3 meses)
- Búsqueda avanzada
- Categorización de documentos
- Notificaciones
- OCR avanzado

### Fase 3: Integraciones (6 meses)
- API para instituciones
- Validación con RENAUT
- Integración CSS/MINSA
- App móvil

---

## 📞 Contacto

- **Email**: info@panamahealth-vault.com
- **GitHub**: [@quantumquirkz](https://github.com/quantumquirkz)

---

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para más detalles.

---

<div align="center">

**PanamaHealth Vault** - Samsung Innovation Campus 2025

*Simple, Local y Funcional* 🚀

</div>
