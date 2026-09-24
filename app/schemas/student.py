from pydantic import BaseModel, EmailStr


class StudentCreate(BaseModel):
    name: str
    age: int
    gender: str
    email: EmailStr
    course: str
    year: int
    phone: str


class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    email: EmailStr
    course: str
    year: int
    phone: str

    class Config:
        from_attributes = True