from sqlalchemy.orm import Session
from teachers import models
from teachers import schemas
from core.cache import redis_client, CACHE_TTL
import json

def get_teacher(db: Session, teacher_id: int):
    teacher_cache = redis_client.get(str(teacher_id))

    if teacher_cache:
        teacher_data = json.loads(teacher_cache)
        return schemas.TeacherResponse(
            id=teacher_id,
            name=teacher_data["name"],
            city=teacher_data["city"],
            program=teacher_data["program"],
            source="redis_cache"
        )
    
    db_teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if db_teacher is None:
        return None
    
    teacher_dict = {
        "name": db_teacher.name,
        "city": db_teacher.city,
        "program": db_teacher.program
    }
    # set with expiration
    redis_client.setex(str(teacher_id), CACHE_TTL, json.dumps(teacher_dict))
    # Para guardarlo sin expiración (para siempre en caché), se usaría set en su lugar:
    # redis_client.set(str(teacher_id), json.dumps(teacher_dict))
    
    return schemas.TeacherResponse(
        id=db_teacher.id,
        name=db_teacher.name,
        city=db_teacher.city,
        program=db_teacher.program,
        source="database"
    )

def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    db_teacher = models.Teacher(name=teacher.name, city=teacher.city, program=teacher.program)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return schemas.TeacherResponse(
        id=db_teacher.id, 
        name=db_teacher.name, 
        city=db_teacher.city, 
        program=db_teacher.program, 
        source="database"
    )

def get_teachers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Teacher).offset(skip).limit(limit).all()
