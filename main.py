
import re
import sqlite3

from fastapi import FastAPI, HTTPException, Query
from ollama import chat

from database import create_table, get_db_connection
from schemas import StudentCreate


app = FastAPI(
    title="Students Database CRUD API",
    description="Student CRUD operations with SQLite and Ollama AI.",
    version="1.0.0",
)


# INITIALIZE DATABASE
@app.on_event("startup")
def startup():
    create_table()


# HOME
@app.get("/")
def home():
    return {"message": "Students Database API is running!"}


# CREATE STUDENT
@app.post("/students", status_code=201)
def create_student(student: StudentCreate):
    connection = get_db_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO students
            (name, date_of_birth, email, phone, course, address, enrollment_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student.name,
                str(student.date_of_birth),
                student.email,
                student.phone,
                student.course,
                student.address,
                str(student.enrollment_date) if student.enrollment_date else None,
            ),
        )

        connection.commit()

        return {
            "message": "Student created successfully",
            "student_id": cursor.lastrowid,
        }

    except sqlite3.IntegrityError as error:
        connection.rollback()

        if "UNIQUE constraint failed: students.email" in str(error):
            raise HTTPException(
                status_code=409,
                detail="A student with this email already exists.",
            )

        raise HTTPException(
            status_code=400,
            detail="Student data violates a database constraint.",
        )

    finally:
        connection.close()


# GET ALL STUDENTS
@app.get("/students")
def get_students():
    connection = get_db_connection()

    try:
        cursor = connection.execute(
            "SELECT * FROM students ORDER BY student_id"
        )
        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


# GET STUDENT BY ID
@app.get("/students/{student_id}")
def get_student_by_id(student_id: int):
    connection = get_db_connection()

    try:
        cursor = connection.execute(
            "SELECT * FROM students WHERE student_id = ?",
            (student_id,),
        )
        student = cursor.fetchone()

        if student is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found",
            )

        return dict(student)

    finally:
        connection.close()


# UPDATE STUDENT
@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentCreate):
    connection = get_db_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE students
            SET name = ?,
                date_of_birth = ?,
                email = ?,
                phone = ?,
                course = ?,
                address = ?,
                enrollment_date = ?
            WHERE student_id = ?
            """,
            (
                
                student.name,
                str(student.date_of_birth),
                student.email,
                student.phone,
                student.course,
                student.address,
                str(student.enrollment_date) if student.enrollment_date else None,
                student_id,
            ),
        )

        if cursor.rowcount == 0:
            connection.rollback()
            raise HTTPException(
                status_code=404,
                detail="Student not found",
            )

        connection.commit()

        return {
            "message": "Student updated successfully",
            "student_id": student_id,
        }

    except HTTPException:
        raise

    except sqlite3.IntegrityError as error:
        connection.rollback()

        if "UNIQUE constraint failed: students.email" in str(error):
            raise HTTPException(
                status_code=409,
                detail="A student with this email already exists.",
            )

        raise HTTPException(
            status_code=400,
            detail="Student data violates a database constraint.",
        )

    finally:
        connection.close()


# DELETE STUDENT
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    connection = get_db_connection()

    try:
        cursor = connection.execute(
            "DELETE FROM students WHERE student_id = ?",
            (student_id,),
        )

        if cursor.rowcount == 0:
            connection.rollback()
            raise HTTPException(
                status_code=404,
                detail="Student not found",
            )

        connection.commit()

        return {
            "message": "Student deleted successfully",
            "student_id": student_id,
        }

    finally:
        connection.close()


# GENERAL OLLAMA AI
@app.post("/ask-ai")
def ask_ai(
    question: str = Query(..., min_length=1, max_length=2000)
):
    try:
        response = chat(
            model="qwen2.5:3b",
            messages=[{"role": "user", "content": question}],
        )

        return {
            "question": question,
            "answer": response.message.content,
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="AI service is unavailable. Check whether Ollama is running.",
        )


# GET STUDENT COUNT
@app.get("/ai/student-count")
def ai_student_count():
    connection = get_db_connection()

    try:
        cursor = connection.execute(
            "SELECT COUNT(*) AS total FROM students"
        )
        result = cursor.fetchone()

        return {"total_students": result["total"]}

    finally:
        connection.close()


# AI WITH STUDENT DATABASE CONTEXT
@app.post("/ask-ai/students")
def ask_ai_about_students(
    question: str = Query(..., min_length=1, max_length=2000)
):
    connection = get_db_connection()

    try:
        cursor = connection.execute(
            """
            SELECT student_id, name, course
            FROM students
            ORDER BY student_id
            """
        )
        students = [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()

    total_students = len(students)
    normalized_question = question.lower()

    # Answer student count questions using actual database data
    count_phrases = [
        "how many students",
        "student count",
        "total students",
        "number of students",
        "kitne students",
        "kitne student",
    ]

    if any(phrase in normalized_question for phrase in count_phrases):
        return {
            "question": question,
            "total_students": total_students,
            "students": students,
            "answer": f"There are {total_students} registered student(s).",
        }

    # Handle explicit student ID lookups using Python
    id_match = re.search(
        r"\b(?:student\s+)?id\s*#?\s*(\d+)\b",
        question,
        re.IGNORECASE,
    )

    if id_match:
        requested_id = int(id_match.group(1))

        matching_student = next(
            (
                student
                for student in students
                if student["student_id"] == requested_id
            ),
            None,
        )

        if matching_student is None:
            return {
                "question": question,
                "total_students": total_students,
                "found": False,
                "answer": f"No student found with ID {requested_id}.",
            }

        return {
            "question": question,
            "total_students": total_students,
            "found": True,
            "student": matching_student,
            "answer": (
                f"Student found: {matching_student['name']}, "
                f"Course: {matching_student['course']}."
            ),
        }

    # Do not ask the model to answer student questions from an empty database
    if not students:
        return {
            "question": question,
            "total_students": 0,
            "answer": "No students are currently registered in the database.",
        }

    # Ask Ollama about the retrieved database records
    try:
        response = chat(
            model="qwen2.5:3b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an assistant for a student database. "
                        "Use only the student records provided below. "
                        "Never invent student details. "
                        "If the requested information is unavailable, "
                        "clearly say it is not present in these records.\n\n"
                        f"Database records: {students}"
                    ),
                },
                {"role": "user", "content": question},
            ],
        )

        return {
            "question": question,
            "total_students": total_students,
            "answer": response.message.content,
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="AI service is unavailable. Check whether Ollama is running.",
        )
