from sqlalchemy.orm import Session

from app.database.models import Student
from app.schemas.student import StudentCreate


def create_student(db: Session, student: StudentCreate):
    db_student = Student(
        name=student.name,
        age=student.age,
        gender=student.gender,
        email=student.email,
        course=student.course,
        year=student.year,
        phone=student.phone
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


def get_students(db: Session):
    return db.query(Student).all()


def get_student(db: Session, student_id: int):
    return db.query(Student).filter(
        Student.id == student_id
    ).first()


def update_student(
    db: Session,
    student_id: int,
    student: StudentCreate
):
    db_student = get_student(db, student_id)

    if db_student is None:
        return None

    db_student.name = student.name
    db_student.age = student.age
    db_student.gender = student.gender
    db_student.email = student.email
    db_student.course = student.course
    db_student.year = student.year
    db_student.phone = student.phone

    db.commit()
    db.refresh(db_student)

    return db_student


def delete_student(db: Session, student_id: int):
    db_student = get_student(db, student_id)

    if db_student is None:
        return None

    db.delete(db_student)
    db.commit()

    return db_student