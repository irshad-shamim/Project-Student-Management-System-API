from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, String, Integer, Column
from sqlalchemy.orm import sessionmaker, declarative_base, Session
app = FastAPI()


DATABASE_URL = "sqlite:///./details.db"

engine = create_engine(
    DATABASE_URL,
    connect_args= {"check_same_thread": False}
)

sessionLocal = sessionmaker(bind=engine)

base = declarative_base()

class Student(base):
    __tablename__ = "All_Students"
    name = Column(String)
    email = Column(String)
    rollno = Column(String, primary_key= True) 
    course = Column(String)
    year = Column(Integer)

base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/new_student")
def add_new_student(name:str, email:str, rollno:str, course:str, year:int, db: Session = Depends(get_db)):
    students = Student(name=name, email=email, rollno=rollno, course=course, year=year)
    db.add(students)
    db.commit()
    db.refresh(students)
    return {
        "message": "new student added secsusfuly...",
        "student": students
    }

@app.get("/all_student")
def all_student(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return {
        "total student": len(students),
        "students details": students
    }

