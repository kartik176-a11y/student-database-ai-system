import re
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.database.connection import SessionLocal
from app.database.models import Student

from app.ai.tools import (
    count_students,
    get_all_students,
    get_student_by_id,
    count_students_by_gender,
    get_students_by_gender,
    get_students_by_course,
    get_students_by_age,
    semantic_student_search
)

from app.ai.chatbot import generate_ai_response


# ==========================================
# CHAT STATE
# ==========================================

class ChatState(TypedDict):
    message: str
    response: str


# ==========================================
# CHATBOT NODE
# ==========================================

def chatbot_node(state: ChatState):

    original_message = state["message"]
    message = original_message.lower().strip()

    db = SessionLocal()

    try:

        # ==========================================
        # STUDENT BY ID
        # ==========================================

        id_match = re.search(
            r"(?:student\s+)?(?:with\s+)?id\s*(?:is\s*)?(\d+)",
            message
        )

        if id_match:

            student_id = int(id_match.group(1))

            student = get_student_by_id(
                db,
                student_id
            )

            if student is None:

                context = (
                    f"Student with ID {student_id} "
                    f"was not found."
                )

            else:

                context = str([student])


        # ==========================================
        # OTHER QUERIES
        # ==========================================

        else:

            # ==========================================
            # GENDER DETECTION
            # ==========================================

            gender = None

            if (
                "female" in message
                or "women" in message
                or "woman" in message
            ):

                gender = "Female"

            elif (
                "male" in message
                or "men" in message
                or "man" in message
            ):

                gender = "Male"


            # ==========================================
            # AGE DETECTION
            # ==========================================

            age = None

            age_match = re.search(
                r"\b(?:aged|age(?:\s+is)?|are)\s*(\d+)\b"
                r"|\b(\d+)\s*(?:years?\s*old|year\s*old)\b",
                message,
                re.IGNORECASE
            )

            if age_match:

                age = int(
                    age_match.group(1)
                    or age_match.group(2)
                )


            # ==========================================
            # COURSE DETECTION
            # ==========================================

            course = None

            if "computer science" in message:

                course = "Computer Science"

            elif (
                "artificial intelligence" in message
                or "ai students" in message
                or "ai course" in message
            ):

                course = "Artificial Intelligence"

            elif (
                "mbbs" in message
                or "medical student" in message
                or "medical students" in message
            ):

                course = "MBBS"

            elif "aerospace" in message:

                course = "Aerospace & Technology"


            # ==========================================
            # GENDER + AGE + COURSE
            # ==========================================

            if (
                gender is not None
                and age is not None
                and course is not None
            ):

                students = (
                    db.query(Student)
                    .filter(
                        Student.gender.ilike(gender),
                        Student.age == age,
                        Student.course.ilike(course)
                    )
                    .all()
                )

                context = str([
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
                ])


            # ==========================================
            # GENDER + AGE
            # ==========================================

            elif (
                gender is not None
                and age is not None
            ):

                students = (
                    db.query(Student)
                    .filter(
                        Student.gender.ilike(gender),
                        Student.age == age
                    )
                    .all()
                )

                context = str([
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
                ])


            # ==========================================
            # GENDER + COURSE
            # ==========================================

            elif (
                gender is not None
                and course is not None
            ):

                students = (
                    db.query(Student)
                    .filter(
                        Student.gender.ilike(gender),
                        Student.course.ilike(course)
                    )
                    .all()
                )

                context = str([
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
                ])


            # ==========================================
            # AGE + COURSE
            # ==========================================

            elif (
                age is not None
                and course is not None
            ):

                students = (
                    db.query(Student)
                    .filter(
                        Student.age == age,
                        Student.course.ilike(course)
                    )
                    .all()
                )

                context = str([
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
                ])


            # ==========================================
            # AGE ONLY
            # ==========================================

            elif age is not None:

                students = get_students_by_age(
                    db,
                    age
                )

                context = str(students)


            # ==========================================
            # GENDER ONLY
            # ==========================================

            elif gender is not None:

                if (
                    "how many" in message
                    or "count" in message
                    or "number" in message
                ):

                    count = count_students_by_gender(
                        db,
                        gender
                    )

                    context = (
                        f"There are {count} "
                        f"{gender.lower()} students "
                        f"in the database."
                    )

                else:

                    students = get_students_by_gender(
                        db,
                        gender
                    )

                    context = str(students)


            # ==========================================
            # COURSE ONLY
            # ==========================================

            elif course is not None:

                students = get_students_by_course(
                    db,
                    course
                )

                context = str(students)


            # ==========================================
            # TOTAL STUDENTS
            # ==========================================

            elif (
                "how many students" in message
                or "total students" in message
                or "number of students" in message
            ):

                count = count_students(db)

                context = (
                    f"There are {count} students "
                    f"in the database."
                )


            # ==========================================
            # ALL STUDENTS
            # ==========================================

            elif (
                "all students" in message
                or "show students" in message
                or "list students" in message
            ):

                students = get_all_students(db)

                context = str(students)


            # ==========================================
            # CHROMADB SEMANTIC SEARCH
            # ==========================================

            else:

                search_results = semantic_student_search(
                    original_message
                )

                context = str({
                    "documents": search_results["documents"],
                    "metadatas": search_results["metadatas"],
                    "distances": search_results["distances"]
                })


        # ==========================================
        # GENERATE RESPONSE
        # ==========================================

        response = generate_ai_response(
            original_message,
            context
        )

        return {
            "message": original_message,
            "response": response
        }


    except Exception as e:

        return {
            "message": original_message,
            "response": (
                "Sorry, I couldn't process your request.\n\n"
                f"Error: {str(e)}"
            )
        }


    finally:

        db.close()


# ==========================================
# LANGGRAPH
# ==========================================

graph_builder = StateGraph(ChatState)


graph_builder.add_node(
    "chatbot",
    chatbot_node
)


graph_builder.add_edge(
    START,
    "chatbot"
)


graph_builder.add_edge(
    "chatbot",
    END
)


student_graph = graph_builder.compile()