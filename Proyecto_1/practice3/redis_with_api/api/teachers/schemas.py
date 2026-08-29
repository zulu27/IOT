from pydantic import BaseModel

class TeacherBase(BaseModel):
    name: str
    city: str
    program: str

class TeacherCreate(TeacherBase):
    pass

class TeacherResponse(TeacherBase):
    id: int
    source: str = "database"
    
    class Config:
        from_attributes = True
