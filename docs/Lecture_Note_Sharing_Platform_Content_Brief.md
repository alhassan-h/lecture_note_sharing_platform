# Lecture Note Sharing Platform – Content Brief

## 1. Project Overview
Build a web-based Lecture Note Sharing Platform that allows lecturers to upload lecture notes and students to view and download them. The system is a proof of concept, not a full Learning Management System (LMS).

---

## 2. Target Users
- Lecturers
- Students
- Admin (optional, minimal role)

---

## 3. Technology Stack
- Backend: Python (Flask)
- Frontend: HTML, Bootstrap 5
- Database: MySQL
- ORM (optional): SQLAlchemy
- Authentication: Flask-Login
- File Storage: Local filesystem (/uploads directory)

---

## 4. Core Functionalities

### 4.1 Authentication & Authorization
- User registration
- User login and logout
- Role-based access control (Lecturer, Student)

Rules:
- Only lecturers can upload notes
- Students can only view and download notes
- Unauthenticated users cannot access protected pages

---

### 4.2 Lecture Note Management
- Upload lecture notes (PDF, DOCX)
- Store metadata:
  - Course title
  - Course code
  - Lecturer name
  - Upload date
- Download lecture notes
- List notes by course

---

### 4.3 Course Management
- Simple course handling
- Courses can be predefined or created during upload

---

## 5. Pages / User Interfaces

### 5.1 Landing Page
- Project title and description
- Login button
- Register button

---

### 5.2 Registration Page
Fields:
- Full name
- Email
- Password
- Role (Lecturer or Student)

Validations:
- Unique email
- Minimum password length

---

### 5.3 Login Page
Fields:
- Email
- Password

Behavior:
- Redirect users based on role after login

---

### 5.4 Lecturer Dashboard
Components:
- Upload lecture note form:
  - Course title
  - Course code
  - File upload
- List of uploaded notes
- Download and optional delete buttons

---

### 5.5 Student Dashboard
Components:
- List or table of available lecture notes
- Search or filter by course
- Download button

---

## 6. UI Design Guidelines
- Use Bootstrap 5
- Clean academic look
- Minimal color scheme
- Responsive layout
- Tables for listing notes
- Alerts for success and error messages

---

## 7. Database Schema

### Users Table
| Field | Type |
|------|------|
| id | INT (Primary Key) |
| name | VARCHAR |
| email | VARCHAR (Unique) |
| password_hash | VARCHAR |
| role | ENUM('lecturer', 'student') |

---

### Notes Table
| Field | Type |
|------|------|
| id | INT (Primary Key) |
| course_title | VARCHAR |
| course_code | VARCHAR |
| filename | VARCHAR |
| uploaded_by | INT (Foreign Key -> users.id) |
| upload_date | DATETIME |

---

## 8. Backend Routes

### Authentication Routes
- /register
- /login
- /logout

---

### Lecturer Routes
- /lecturer/dashboard
- /notes/upload
- /notes/delete/<id>

---

### Student Routes
- /student/dashboard
- /notes/download/<id>

---

## 9. Security Considerations
- Password hashing using Werkzeug
- File type validation
- Protected routes using decorators
- No public access to uploaded files

---

## 10. Project Folder Structure

```
project/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── lecturer.py
│   │   └── student.py
│   ├── templates/
│   ├── static/
│
├── uploads/
├── config.py
├── run.py
```

---

## 11. Out of Scope
- Real-time chat
- Notifications
- Grading system
- Email verification
- Cloud storage

---

## 12. Success Criteria
The system is successful if:
- Users can register and log in
- Lecturers can upload lecture notes
- Students can download lecture notes
- Role-based access control works
- UI is clean and usable

---

## 13. Notes to Coding Agent
- Keep implementation simple
- Prioritize clarity and readability
- This is a demo system, not production-ready
- Follow the structure defined in this brief
