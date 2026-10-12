
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import sqlite3

app = FastAPI(
    title="Students Database CRUD API",
    description="A simple student management system",
    version="1.0.0"
)

DATABASE = "students.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                course TEXT NOT NULL
            )
        """)


create_table()


class Student(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(gt=0, le=120)
    course: str = Field(min_length=1, max_length=100)


@app.get("/")
def home():
    return {"message": "Students Database CRUD API is running!"}


@app.post("/students", status_code=201)
def create_student(student: Student):
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
            (student.name, student.age, student.course)
        )
        student_id = cursor.lastrowid

    return {"message": "Student created", "id": student_id}


@app.get("/students")
def get_students():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM students ORDER BY id"
        ).fetchall()

    return [dict(row) for row in rows]


@app.get("/students/{student_id}")
def get_student(student_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return dict(row)


@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE students SET name = ?, age = ?, course = ? WHERE id = ?",
            (student.name, student.age, student.course, student_id)
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student updated"}


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student deleted"}
