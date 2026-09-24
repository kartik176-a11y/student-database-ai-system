from app.config import GEMINI_API_KEY
import ast
import re


# ==========================================
# FORMAT ONE STUDENT
# ==========================================

def format_student(student, index):

    return (
        f"{index}. {student.get('name', 'Unknown')}\n"
        f"   Age: {student.get('age', 'N/A')}\n"
        f"   Gender: {student.get('gender', 'N/A')}\n"
        f"   Course: {student.get('course', 'N/A')}\n"
        f"   Year: {student.get('year', 'N/A')}\n"
        f"   Email: {student.get('email', 'N/A')}\n"
        f"   Phone: {student.get('phone', 'N/A')}"
    )


# ==========================================
# PARSE CHROMADB CONTEXT
# ==========================================

def parse_chroma_context(context):
    """
    Convert ChromaDB documents into clean
    student dictionaries.
    """

    try:

        data = ast.literal_eval(context)

        if not isinstance(data, dict):
            return []

        documents = data.get("documents", [])

        if not documents:
            return []

        documents = documents[0]

        students = []

        for document in documents:

            match = re.search(
                r"Student Name: (.*?)\. Age: (.*?)\. Gender: (.*?)\. "
                r"Email: (.*?)\. Course: (.*?)\. Year: (.*?)\. "
                r"Phone: (.*?)\.",
                document
            )

            if match:

                students.append({
                    "name": match.group(1),
                    "age": match.group(2),
                    "gender": match.group(3),
                    "email": match.group(4),
                    "course": match.group(5),
                    "year": match.group(6),
                    "phone": match.group(7)
                })

        return students

    except Exception:

        return []


# ==========================================
# FORMAT DATABASE RESPONSE
# ==========================================

def format_database_response(
    message,
    context
):

    # ==========================================
    # COUNT RESPONSE
    # ==========================================

    if context.startswith("There are"):

        return context


    # ==========================================
    # NORMAL DATABASE STUDENT LIST
    # ==========================================

    if context.startswith("["):

        try:

            students = ast.literal_eval(context)

            # Empty result
            if isinstance(students, list) and not students:

                return "No students matched your criteria."


            # Students found
            if isinstance(students, list) and students:

                response = (
                    f"I found {len(students)} student"
                    f"{'s' if len(students) != 1 else ''}:\n\n"
                )

                for index, student in enumerate(
                    students,
                    start=1
                ):

                    if isinstance(student, dict):

                        response += (
                            format_student(
                                student,
                                index
                            )
                            + "\n\n"
                        )

                return response.strip()

        except Exception:

            pass


    # ==========================================
    # CHROMADB SEMANTIC SEARCH
    # ==========================================

    if "'documents':" in context:

        students = parse_chroma_context(
            context
        )

        if students:

            response = (
                f"I found {len(students)} relevant student"
                f"{'s' if len(students) != 1 else ''}:\n\n"
            )

            for index, student in enumerate(
                students,
                start=1
            ):

                response += (
                    format_student(
                        student,
                        index
                    )
                    + "\n\n"
                )

            return response.strip()

        else:

            return "No relevant students were found."


    # ==========================================
    # NOT FOUND RESPONSE
    # ==========================================

    if "was not found" in context:

        return context


    # ==========================================
    # FALLBACK
    # ==========================================

    return (
        "Here is the information from the "
        "student database:\n\n"
        + context
    )


# ==========================================
# GENERATE AI RESPONSE
# ==========================================

def generate_ai_response(
    message,
    context
):

    # ==========================================
    # GEMINI NOT CONFIGURED
    # ==========================================

    if not GEMINI_API_KEY:

        return format_database_response(
            message,
            context
        )


    # ==========================================
    # GEMINI
    # ==========================================

    try:

        from google import genai

        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        prompt = f"""
You are a Student Database AI Assistant.

Answer the user's question using only
the database information provided.

User question:
{message}

Database information:
{context}

Rules:
- Do not invent information.
- Give a clear answer.
- Use numbered lists when listing students.
- Do not expose Python dictionaries.
- Do not expose ChromaDB metadata or distances.
- If the database information is an empty list,
  say that no students matched the criteria.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text


    except Exception:

        return format_database_response(
            message,
            context
        )