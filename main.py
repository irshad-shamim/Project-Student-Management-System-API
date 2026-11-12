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

@app.get("/one_student/{student_rollno}")
def one_student(student_rollno: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.rollno == student_rollno).first()
    if not student:
        raise HTTPException(
            status_code= 404,
            detail = f"student not found of rollno {student_rollno}"
        )
    return{
        "student found sescussfuly": student
    }

@app.get("/student_name/{student_name}")
def one_student_by_name(student_name: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.name == student_name).first()
    if not student:
        raise HTTPException(
            status_code= 404,
            detail= f"student of name {student_name} is not avialaible"
        )
    return {
        "student found seccussfully": student
    }

@app.put("/student_update/{student_rollno}")
def student_update(student_rollno:str, name:str, email:str, course:str, year:int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.rollno == student_rollno).first()
    if not student :
        raise HTTPException (
            status_code= 404,
            detail= f"no student found of rollno {student_rollno}"
        )
    student.name = name
    student.emai = email
    student.rollno = student_rollno
    student.course = course
    student.year = year

    db.commit()
    db.refresh(student)
    return{
        "updated status":"secsusfuly",
        "new": student
    }
