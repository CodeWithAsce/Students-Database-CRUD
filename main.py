
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
from datetime import date
import sqlite3

app = FastAPI(
    title="Students Database CRUD API",
    description="Student management using FastAPI and SQLite",
    version="1.0.0"
)

DATABASE = "students.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    with get_connection() as conn:
        columns = conn.execute(
            "PRAGMA table_info(students)"
        ).fetchall()

        if not columns:
            conn.execute("""
                CREATE TABLE students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    date_of_birth TEXT NOT NULL,
                    email TEXT NOT NULL,
                    course TEXT NOT NULL
                )
            """)
            return

        existing_columns = {row["name"] for row in columns}

        # Migrate old database safely when age is present
        if "age" in existing_columns:
            conn.execute("""
                CREATE TABLE students_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    date_of_birth TEXT,
                    email TEXT,
                    course TEXT NOT NULL
                )
            """)

            conn.execute("""
                INSERT INTO students_new (id, name, course)
                SELECT id, name, course FROM students
            """)

            conn.execute("DROP TABLE students")
            conn.execute("ALTER TABLE students_new RENAME TO students")

        else:
            if "date_of_birth" not in existing_columns:
                conn.execute(
                    "ALTER TABLE students ADD COLUMN date_of_birth TEXT"
                )

            if "email" not in existing_columns:
                conn.execute(
                    "ALTER TABLE students ADD COLUMN email TEXT"
                )


create_table()


class Student(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    date_of_birth: date
    email: EmailStr
    course: str = Field(min_length=1, max_length=100)


@app.get("/")
def home():
    return {"message": "Students Database CRUD API is running!"}


@app.post("/students", status_code=201)
def create_student(student: Student):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO students (name, date_of_birth, email, course)
            VALUES (?, ?, ?, ?)
            """,
            (
                student.name,
                student.date_of_birth.isoformat(),
                str(student.email),
                student.course
            )
        )

        student_id = cursor.lastrowid

    return {"message": "Student created", "id": student_id}



@app.get("/students")
def get_students(course: str | None = None):
    with get_connection() as conn:
        if course:
            rows = conn.execute(
                "SELECT * FROM students WHERE course = ? ORDER BY id",
                (course,)
            ).fetchall()
        else:
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
            """
            UPDATE students
            SET name = ?, date_of_birth = ?, email = ?, course = ?
            WHERE id = ?
            """,
            (
                student.name,
                student.date_of_birth.isoformat(),
                str(student.email),
                student.course,
                student_id
            )
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
