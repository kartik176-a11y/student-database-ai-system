from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.student import StudentCreate, StudentResponse
from app.services.student_service import (
    create_student,
    get_students,
    get_student,
    update_student,
    delete_student
)

router = APIRouter(
    prefix="/students",
    tags=["👨‍🎓 Students"]
)


@router.post(
    "/",
    response_model=StudentResponse,
    summary="➕ Add a Student",
    description="Create a new student record in the database."
)
def add_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    return create_student(db, student)


@router.get(
    "/",
    response_model=list[StudentResponse],
    summary="📋 Get All Students",
    description="Retrieve all students from the database."
)
def read_students(
    db: Session = Depends(get_db)
):
    return get_students(db)


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    summary="🔍 Get Student",
    description="Retrieve a student using their ID."
)
def read_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = get_student(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    summary="✏️ Update Student",
    description="Update an existing student's information."
)
def edit_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    updated_student = update_student(
        db,
        student_id,
        student
    )

    if updated_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return updated_student


@router.delete(
    "/{student_id}",
    summary="🗑️ Delete Student",
    description="Delete a student from the database."
)
def remove_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    deleted_student = delete_student(
        db,
        student_id
    )

    if deleted_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student deleted successfully"
    }