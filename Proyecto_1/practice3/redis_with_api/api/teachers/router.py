from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from teachers import service
from teachers import schemas
from core.database import get_db

router = APIRouter(
    prefix="/teachers",
    tags=["teachers"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.TeacherResponse)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    return service.create_teacher(db=db, teacher=teacher)

@router.get("/{teacher_id}", response_model=schemas.TeacherResponse)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher_response = service.get_teacher(db=db, teacher_id=teacher_id)
    if teacher_response is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher_response

@router.get("/", response_model=List[schemas.TeacherResponse])
def list_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teachers = service.get_teachers(db, skip=skip, limit=limit)
    
    return [
        schemas.TeacherResponse(
            id=t.id,
            name=t.name,
            city=t.city,
            program=t.program,
            source="database"
        ) for t in teachers
    ]
