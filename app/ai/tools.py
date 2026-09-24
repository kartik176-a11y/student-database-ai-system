from sqlalchemy.orm import Session

from app.database.models import Student

from app.vector_db.chroma_db import search_documents


# ==========================================
# COUNT ALL STUDENTS
# ==========================================

def count_students(db: Session):
    return db.query(Student).count()


# ==========================================
# GET ALL STUDENTS
# ==========================================

def get_all_students(db: Session):

    students = db.query(Student).all()

    return [
        {
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "gender": student.gender,
            "email": student.email,
            "course": student.course,
            "year": student.year,
            "phone": student.phone
        }
        for student in students
    ]


# ==========================================
# GET STUDENT BY ID
# ==========================================

def get_student_by_id(
    db: Session,
    student_id: int
):

    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if student is None:
        return None

    return {
        "id": student.id,
        "name": student.name,
        "age": student.age,
        "gender": student.gender,
        "email": student.email,
        "course": student.course,
        "year": student.year,
        "phone": student.phone
    }


# ==========================================
# COUNT STUDENTS BY GENDER
# ==========================================

def count_students_by_gender(
    db: Session,
    gender: str
):

    return (
        db.query(Student)
        .filter(Student.gender.ilike(gender))
        .count()
    )


# ==========================================
# GET STUDENTS BY GENDER
# ==========================================

def get_students_by_gender(
    db: Session,
    gender: str
):

    students = (
        db.query(Student)
        .filter(Student.gender.ilike(gender))
        .all()
    )

    return [
        {
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "gender": student.gender,
            "email": student.email,
            "course": student.course,
            "year": student.year,
            "phone": student.phone
        }
        for student in students
    ]


# ==========================================
# GET STUDENTS BY COURSE
# ==========================================

def get_students_by_course(
    db: Session,
    course: str
):

    students = (
        db.query(Student)
        .filter(Student.course.ilike(course))
        .all()
    )

    return [
        {
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "gender": student.gender,
            "email": student.email,
            "course": student.course,
            "year": student.year,
            "phone": student.phone
        }
        for student in students
    ]


# ==========================================
# GET STUDENTS BY AGE
# ==========================================

def get_students_by_age(
    db: Session,
    age: int
):

    students = (
        db.query(Student)
        .filter(Student.age == age)
        .all()
    )

    return [
        {
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "gender": student.gender,
            "email": student.email,
            "course": student.course,
            "year": student.year,
            "phone": student.phone
        }
        for student in students
    ]


# ==========================================
# SEMANTIC STUDENT SEARCH
# ==========================================

def semantic_student_search(
    query: str
):

    results = search_documents(query)

    return {
        "documents": results["documents"],
        "metadatas": results["metadatas"],
        "distances": results["distances"]
    }