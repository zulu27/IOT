from fastapi import FastAPI
from core.database import engine, Base

# Importar modelos para que SQLAlchemy los registre
from students import models as student_models
from teachers import models as teacher_models

from students import router as students_router
from teachers import router as teachers_router

# Crear las tablas en la BD (Base de core.database)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="University API with Redis Cache")

app.include_router(students_router.router)
app.include_router(teachers_router.router)
