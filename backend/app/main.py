from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .config import settings
from .database import init_db

# Importar routers cuando estén listos
# from app.routers import auth, users, records, permissions

app = FastAPI(
    title="PanamaHealth Vault API",
    description="API para gestión de expedientes médicos digitales (Local)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar carpeta de uploads (para servir archivos)
app.mount("/uploads", StaticFiles(directory=str(settings.UPLOAD_DIR)), name="uploads")


@app.on_event("startup")
async def startup_event():
    """Inicializar aplicación"""
    print("🚀 Iniciando PanamaHealth Vault API...")
    print(f"📁 Directorio de uploads: {settings.UPLOAD_DIR}")
    print(f"💾 Base de datos: {settings.DATABASE_URL}")
    
    # Inicializar base de datos
    init_db()
    
    print("✅ API lista en http://localhost:8000")
    print("📚 Documentación en http://localhost:8000/docs")


@app.get("/")
async def root():
    """Endpoint raíz - Health check"""
    return {
        "message": "PanamaHealth Vault API",
        "status": "online",
        "version": "1.0.0",
        "mode": "local",
        "database": "SQLite",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    return {
        "status": "healthy",
        "database": "sqlite",
        "uploads_dir": str(settings.UPLOAD_DIR)
    }


# Incluir routers cuando estén implementados
# app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
# app.include_router(users.router, prefix="/api/users", tags=["Users"])
# app.include_router(records.router, prefix="/api/records", tags=["Medical Records"])
# app.include_router(permissions.router, prefix="/api/permissions", tags=["Permissions"])


# Manejador de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("🏥 PanamaHealth Vault - Modo Local")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

