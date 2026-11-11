from pydantic import BaseModel


class Student(BaseModel):
    name: str
    email: str
    rollno: str
    course: str
    year: int