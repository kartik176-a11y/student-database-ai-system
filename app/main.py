from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database.connection import Base, engine
from app.database.models import Student
from app.routes.students import router as student_router
from app.routes.chat import router as chat_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="🎓 Student Database AI",
    description="""
# 🎓 Student Database Application

A modern backend API for managing student records.

### 🚀 Features

- 👨‍🎓 Student Management
- ➕ Create Students
- 📋 View Students
- 🔍 Search Student by ID
- ✏️ Update Student
- 🗑️ Delete Student
- 🤖 AI Chatbot integration
- 🧠 Gemini + LangGraph
- 🗄️ Database interaction

### 🛠️ Technology Stack

**FastAPI • Python • SQLite • SQLAlchemy • Gemini • LangGraph**
""",
    version="1.0.0",
    contact={
        "name": "Student Database AI Project"
    },
    license_info={
        "name": "MIT"
    }
)


# Register student routes
app.include_router(student_router)
app.include_router(chat_router)


app.mount(
    "/ui",
    StaticFiles(
        directory="frontend",
        html=True
    ),
    name="frontend"
)


@app.get(
    "/",
    tags=["🏠 Home"],
    summary="API Health Check",
    description="Check whether the Student Database API is running."
)
def root():
    return {
        "status": "success",
        "message": "🎓 Student Database API is running!",
        "version": "1.0.0"
    }