from pydantic import BaseModel

class StudentBase(BaseModel):
    name: str
    city: str
    program: str

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    source: str = "database"
    
    class Config:
        from_attributes = True
