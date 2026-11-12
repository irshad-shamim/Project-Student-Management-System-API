from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, String, Integer, Column
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from password import create_token, verify_token
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
def add_new_student(name:str, email:str, rollno:str, course:str, year:int, db: Session = Depends(get_db), user = Depends(verify_token)):
    students = Student(name=name, email=email, rollno=rollno, course=course, year=year)
    if db.query(Student).filter(Student.rollno == rollno).first():
        raise HTTPException(
            status_code=404,
            detail = "already rollno exist"
        )
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
    student = db.query(Student).filter(Student.name == student_name).all()
    if not student:
        raise HTTPException(
            status_code= 404,
            detail= f"student of name {student_name} is not avialaible"
        )
    return {
        "student found seccussfully": student
    }

@app.put("/student_update/{student_rollno}")
def student_update(student_rollno:str, name:str | None = None, email:str | None = None, course:str | None = None, year:int | None = None, db: Session = Depends(get_db), user = Depends(verify_token)):
    student = db.query(Student).filter(Student.rollno == student_rollno).first()
    if not student :
        raise HTTPException (
            status_code= 404,
            detail= f"no student found of rollno {student_rollno}"
        )
    
    if name != None:
        student.name = name
    if email != None:
        student.email = email
    if course != None:
        student.course = course
    if year != None:
        student.year = year

    db.commit()
    db.refresh(student)
    return{
        "updated status":"secsusfuly",
        "new": student
    }

@app.delete("/delete_student/{student_rollno}")
def delete_student(student_rollno:str, db: Session = Depends(get_db), user=Depends(verify_token)):
    student = db.query(Student).filter(Student.rollno == student_rollno).first()
    if not student:
        raise HTTPException(
            status_code = 409,
            detail = f"student not found of rollno {student_rollno}"
        )

    db.delete(student)
    db.commit()

    return{
        "status":"deleted seccusfully",
        "student": student
    }


#___________________login___________________________

@app.post("/login")
def login(username:str, password:str):
    if username != "irshad" or password != "pich":
        raise HTTPException(
            status_code= 401,
            detail= "wrong password and user name"
        )
    token = create_token({
        "sub": username
    })
    return {
        "token": token
    }