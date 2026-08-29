from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from students import service
from students import schemas
from core.database import get_db

router = APIRouter(
    prefix="/students",
    tags=["students"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return service.create_student(db=db, student=student)

@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student_response = service.get_student(db=db, student_id=student_id)
    if student_response is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_response

@router.get("/", response_model=List[schemas.StudentResponse])
def list_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = service.get_students(db, skip=skip, limit=limit)
    
    # Mapear los modelos de SQLAlchemy a la respuesta esperada por Pydantic
    return [
        schemas.StudentResponse(
            id=s.id,
            name=s.name,
            city=s.city,
            program=s.program,
            source="database"
        ) for s in students
    ]
