from sqlalchemy.orm import Session
from students import models
from students import schemas
from core.cache import redis_client, CACHE_TTL
import json

def get_student(db: Session, student_id: int):
    # 1. Intentar obtener de Redis (caché)
    student_cache = redis_client.get(str(student_id))

    if student_cache:
        # Cache hit
        student_data = json.loads(student_cache)
        return schemas.StudentResponse(
            id=student_id,
            name=student_data["name"],
            city=student_data["city"],
            program=student_data["program"],
            source="redis_cache"
        )
    
    # 2. Si no está en Redis, buscar en PostgreSQL
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        return None
    
    # 3. Guardar en Redis para futuras consultas
    student_dict = {
        "name": db_student.name,
        "city": db_student.city,
        "program": db_student.program
    }
    # set with expiration
    redis_client.setex(str(student_id), CACHE_TTL, json.dumps(student_dict))
    # Para guardarlo sin expiración (para siempre en caché), se usaría set en su lugar:
    # redis_client.set(str(student_id), json.dumps(student_dict))
    
    return schemas.StudentResponse(
        id=db_student.id,
        name=db_student.name,
        city=db_student.city,
        program=db_student.program,
        source="database"
    )

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(name=student.name, city=student.city, program=student.program)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return schemas.StudentResponse(
        id=db_student.id, 
        name=db_student.name, 
        city=db_student.city, 
        program=db_student.program, 
        source="database"
    )

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()
