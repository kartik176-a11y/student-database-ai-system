from app.database.connection import SessionLocal
from app.database.models import Student
from app.vector_db.chroma_db import add_document


def load_students():
    db = SessionLocal()

    try:
        students = db.query(Student).all()

        for student in students:
            document = (
                f"Student Name: {student.name}. "
                f"Age: {student.age}. "
                f"Gender: {student.gender}. "
                f"Email: {student.email}. "
                f"Course: {student.course}. "
                f"Year: {student.year}. "
                f"Phone: {student.phone}."
            )

            metadata = {
                "student_id": str(student.id),
                "course": student.course,
                "gender": student.gender
            }

            add_document(
                document_id=str(student.id),
                document=document,
                metadata=metadata
            )

        print(f"Loaded {len(students)} students into ChromaDB.")

    finally:
        db.close()


if __name__ == "__main__":
    load_students()