# 🎓 Student Database AI System

An AI-powered **Student Database Application System** built with **FastAPI, SQLite, SQLAlchemy, LangGraph, ChromaDB, and a conversational AI chatbot**.

The system provides REST APIs for student management and an AI assistant that can interact with the student database using natural-language queries.

## 🚀 Features

- 👨‍🎓 Student management system
- ➕ Add students
- 📋 View all students
- 🔍 Search students by ID
- ✏️ Update student information
- 🗑️ Delete students
- 🤖 AI-powered conversational chatbot
- 🧠 LangGraph-based chatbot workflow
- 🔎 Natural-language student search
- 🗄️ SQLite database with SQLAlchemy ORM
- 🧬 ChromaDB vector database
- 🔍 Semantic student search
- 🎯 Exact filtering by age, gender, and course
- 🔗 Combined filtering such as:
  - Female students aged 19
  - Male students aged 20
  - Students aged 20 studying Computer Science
  - Female students studying Artificial Intelligence
- 📖 Interactive Swagger API documentation
- 🌐 Simple web frontend
- 🔐 Environment-variable based API key configuration

## 🏗️ Project Architecture

```text
student-database-ai-system/
│
├── app/
│   ├── ai/
│   │   ├── chatbot.py
│   │   ├── graph.py
│   │   └── tools.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── models.py
│   │
│   ├── routes/
│   │   ├── chat.py
│   │   └── students.py
│   │
│   ├── schemas/
│   │   ├── chat.py
│   │   └── student.py
│   │
│   ├── services/
│   │   └── student_service.py
│   │
│   ├── vector_db/
│   │   ├── chroma_db.py
│   │   └── load_students.py
│   │
│   ├── config.py
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── .gitignore
├── README.md
└── requirements.txt
```

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | Backend REST API |
| SQLite | Relational database |
| SQLAlchemy | ORM and database interaction |
| Pydantic | Data validation |
| LangGraph | AI workflow orchestration |
| Gemini | AI response generation |
| ChromaDB | Vector database and semantic search |
| HTML/CSS/JavaScript | Frontend |
| Uvicorn | ASGI server |
| Git & GitHub | Version control |

## 📡 API Endpoints

### Student APIs

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/students/` | Create a student |
| `GET` | `/students/` | Get all students |
| `GET` | `/students/{student_id}` | Get student by ID |
| `PUT` | `/students/{student_id}` | Update student |
| `DELETE` | `/students/{student_id}` | Delete student |

### AI Chatbot

```text
POST /chat/
```

The chatbot accepts natural-language questions and returns information from the student database.

## 🤖 Example AI Queries

```text
How many students are there?
```

```text
Show all students
```

```text
Show student with ID 6
```

```text
Find female students aged 19
```

```text
Find male students aged 20
```

```text
Find students aged 20 studying Computer Science
```

```text
Find female students studying Artificial Intelligence
```

```text
Find students studying MBBS
```

The system uses **exact database filtering** for structured attributes such as age, gender, course, and student ID, while ChromaDB is used for semantic search.

## 🔎 ChromaDB Semantic Search

Student information can be stored as vector-search documents in ChromaDB.

The project includes:

```text
app/vector_db/chroma_db.py
```

for ChromaDB operations and:

```text
app/vector_db/load_students.py
```

for loading student information from SQLite into ChromaDB.

Run the loader with:

```bash
python -m app.vector_db.load_students
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/kartik176-a11y/student-database-ai-system.git
cd student-database-ai-system
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
```

The `.env` file should **not** be committed to GitHub.

## ▶️ Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

## 📖 Swagger API Documentation

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

## 🌐 Frontend

The frontend is served through FastAPI.

Open:

```text
http://127.0.0.1:8000/ui/
```

## 🧠 AI Architecture

```text
User
  │
  ▼
Chat Interface
  │
  ▼
FastAPI Chat Endpoint
  │
  ▼
LangGraph
  │
  ├── Student ID Detection
  ├── Gender Detection
  ├── Age Detection
  ├── Course Detection
  │
  ▼
Database Tools
  │
  ├── SQLite + SQLAlchemy
  │
  └── ChromaDB Semantic Search
  │
  ▼
AI Response Generator
  │
  ▼
Chatbot Response
```

## 🔐 Security

Sensitive configuration such as API keys is stored using environment variables.

The following files/directories are excluded from Git:

```text
.env
venv/
__pycache__/
students.db
chroma_data/
```

## 📊 Database

The system uses SQLite with SQLAlchemy ORM.

The student model contains:

```text
id
name
age
gender
email
course
year
phone
```

## 🧪 Testing

The application was tested for:

- Student creation
- Student retrieval
- Student update
- Student deletion
- Student lookup by ID
- Gender filtering
- Age filtering
- Course filtering
- Combined filtering
- Student counting
- ChromaDB loading
- Semantic search
- AI chatbot responses

Example:

```text
Query:
Find female students aged 19

Result:
Monica
Age: 19
Gender: Female
Course: MBBS
```

## 📁 Requirements

Python dependencies are listed in:

```text
requirements.txt
```

Install them using:

```bash
pip install -r requirements.txt
```

## 👨‍💻 Author

**V Karthik**

B.Tech Student  
Computer Science / Cyber & AI

## 📌 Project Status

**Completed — Backend, AI chatbot, database integration, vector search, frontend, testing, and GitHub setup.**

## ⭐ Repository

GitHub:

https://github.com/kartik176-a11y/student-database-ai-system

If you find this project useful, consider giving the repository a ⭐.
