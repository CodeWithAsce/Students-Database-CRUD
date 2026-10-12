# Students Database CRUD Application

A student management REST API built using Python, FastAPI, and SQLite.

## Features

- Create a student record
- View all students
- View a student by ID
- Update student details
- Delete a student record
- Validate email addresses and dates of birth
- Store student data in an SQLite database

## Technologies Used

- Python
- FastAPI
- SQLite
- Pydantic
- Uvicorn

## Project Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Students-Database-CRUD
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository's actual URL.

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m uvicorn main:app --reload
```

### 5. Open the API documentation

Visit:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/students` | Create a student |
| GET | `/students` | List all students |
| GET | `/students/{student_id}` | Get a student by ID |
| PUT | `/students/{student_id}` | Update a student |
| DELETE | `/students/{student_id}` | Delete a student |

## Example Request

Use this JSON body with `POST /students`:

```json
{
  "name": "Rahul Sharma",
  "date_of_birth": "2005-08-15",
  "email": "rahul.test@example.com",
  "course": "B.Tech CSE"
}
```

## Database

Student records are stored in an SQLite database named `students.db`. The application initializes the database when it starts.

## Note

Do not upload the virtual environment, Python cache folders, database files, or database backups to GitHub.

## Author

Student Project — Python Backend Development
