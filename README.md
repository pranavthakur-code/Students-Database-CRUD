# Students Database CRUD API with Ollama AI

## 📌 Project Overview

Students Database CRUD API is a Python-based REST API developed using FastAPI and SQLite. It allows users to create, retrieve, update, and delete student records.

The project also includes optional AI integration using Ollama and a locally running language model. The AI endpoints can answer general questions and respond to questions about student records stored in the database.

This project was developed as part of an AI Agents Internship assignment.

## 🎯 Objectives

- Build a REST API using FastAPI.
- Perform CRUD operations on student records.
- Store data using SQLite.
- Validate input data using Pydantic.
- Prevent duplicate email addresses.
- Handle errors with appropriate HTTP status codes.
- Integrate a local AI model using Ollama.
- Test endpoints using Swagger UI.

## 🛠️ Technologies Used

- Python
- FastAPI
- SQLite
- Pydantic
- Uvicorn
- Ollama
- Qwen 2.5 (3B) language model
- Swagger UI

## ✨ Features

- Create new student records.
- Retrieve all students or search by student ID.
- Update existing student information.
- Delete student records.
- Validate email addresses and input fields.
- Prevent duplicate email addresses.
- Handle missing student records.
- Ask general questions using a local AI model.
- Ask AI questions about student records.
- Retrieve the total student count.
- Test endpoints interactively through Swagger UI.

## 📋 Student Information

Each record can contain:

- Student ID (automatically generated)
- Name
- Date of Birth
- Email
- Phone
- Course
- Address
- Enrollment Date

## 📁 Project Structure

```text
Students-Database-CRUD/
├── main.py
├── database.py
├── schemas.py
├── requirements.txt
├── README.md
├── .gitignore
└── students.db  # Generated locally; not committed
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Students-Database-CRUD
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository URL.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Python Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Install and Start Ollama

Install Ollama for Windows from:

https://ollama.com/download

Download the model:

```bash
ollama pull qwen2.5:3b
```

Make sure Ollama is running locally and the model is available before testing the AI endpoints. The CRUD endpoints do not require the AI model.

### 6. Start the API

```bash
python -m uvicorn main:app --reload
```

### 7. Open Swagger UI

Visit:

http://127.0.0.1:8000/docs

Use Swagger UI to test the API endpoints.

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| POST | `/students` | Create a student |
| GET | `/students` | Retrieve all students |
| GET | `/students/{student_id}` | Retrieve a student by ID |
| PUT | `/students/{student_id}` | Update a student |
| DELETE | `/students/{student_id}` | Delete a student |
| POST | `/ask-ai` | Ask a general AI question |
| GET | `/ai/student-count` | Get the total student count |
| POST | `/ask-ai/students` | Ask questions about student records |

## 🧪 Testing

Test the endpoints using Swagger UI at `/docs`.

Suggested tests:

- Create a student successfully.
- Retrieve all student records.
- Retrieve a student by ID.
- Update a student.
- Delete a student.
- Reject duplicate email addresses.
- Return an error when a student does not exist.
- Validate invalid input data.
- Ask a general question using Ollama.
- Ask AI questions about student records.
- Verify the total student count.

## 🗄️ Database

The application uses SQLite to store student records. The database table is created automatically when the application starts.

- `student_id` is an auto-incrementing primary key.
- `email` must be unique.
- Student data is stored locally in `students.db`.

The database file is excluded from Git using `.gitignore`. New users will create their own database when they start the application.

## 🤖 AI Integration

Ollama provides local language-model inference. The application uses the Qwen 2.5 3B model for AI responses.

The student-focused AI endpoint uses database information to answer relevant questions. Application logic handles supported deterministic queries, such as student ID lookups, before relying on the language model.

## 🚀 Future Improvements

- Add authentication and authorization.
- Add automated tests using Pytest.
- Improve logging and error handling.
- Develop a frontend interface.
- Add pagination and filtering.
- Improve AI response validation.

## 👨‍💻 Author

Developed as part of an AI Agents Internship assignment.
