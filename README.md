# Students Database CRUD Application

## Project Overview
This project is a Student Management REST API developed using Python, FastAPI, and SQLite. It allows users to create, view, update, and delete student records.

## Technologies Used
- Python
- FastAPI
- SQLite
- Uvicorn
- Pydantic

## Features
- Create a new student record
- View all student records
- View a student by ID
- Update student details
- Delete a student record
- Validate student input
- Store records in an SQLite database

## Project Structure
- `main.py` — API endpoints and database operations
- `students.db` — SQLite database, created automatically
- `requirements.txt` — Python dependencies
- `README.md` — Project documentation

## Requirements
- Python 3.14 or compatible Python version
- pip

## Installation and Setup

Open the terminal in the project directory and run:

```powershell
py -m venv .venv
```

Install the dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the Application

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open the interactive API documentation in your browser:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| POST | `/students` | Create a student |
| GET | `/students` | Retrieve all students |
| GET | `/students/{student_id}` | Retrieve one student |
| PUT | `/students/{student_id}` | Update a student |
| DELETE | `/students/{student_id}` | Delete a student |

## Example Student Data

```json
{
  "name": "Aman Kumar",
  "age": 20,
  "course": "B.Tech CSE"
}
```

## Testing
The API endpoints can be tested using the interactive Swagger UI at `/docs`.

## Learning Outcome
This project demonstrates REST API development, database integration, CRUD operations, and input validation using Python.

## Author
Student Developer
