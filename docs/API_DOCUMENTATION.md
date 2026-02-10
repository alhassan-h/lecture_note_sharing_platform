# Lecture Note Sharing Platform - API & Routes Documentation

## Overview
This document describes all routes and endpoints in the LNSP system.

---

## Public Routes (No Authentication Required)

### GET `/`
**Landing Page**
- **Template**: `index.html`
- **Description**: Main landing page with project overview
- **Content**: Project title, description, and action buttons
- **Authenticated Users**: Buttons redirect to dashboards based on role
- **Unauthenticated Users**: Buttons redirect to login/register

---

### GET `/register`
**Registration Form (Display)**
- **Template**: `register.html`
- **Description**: User registration form
- **Fields**: Name, Email, Password, Confirm Password, Role selector
- **Roles**: Lecturer or Student
- **Redirect**: If already logged in, redirects to appropriate dashboard

---

### POST `/register`
**User Registration (Process)**
- **Parameters**:
  - `name` (required): Full name
  - `email` (required): Email address (must be unique)
  - `password` (required): Minimum 6 characters
  - `confirm_password` (required): Must match password
  - `role` (required): 'lecturer' or 'student'

- **Validation**:
  - All fields required
  - Password minimum 6 characters
  - Passwords must match
  - Email must be unique
  - Role must be valid

- **Success**: Flash "Registration successful!" and redirect to login
- **Error**: Flash error message and redirect to register form
- **Database**: Creates new User record with hashed password

---

### GET `/login`
**Login Form (Display)**
- **Template**: `login.html`
- **Description**: User login form
- **Fields**: Email, Password
- **Redirect**: If already logged in, redirects to appropriate dashboard

---

### POST `/login`
**User Login (Process)**
- **Parameters**:
  - `email` (required): Registered email
  - `password` (required): Account password

- **Validation**:
  - Email and password required
  - Credentials must match database

- **Success**: 
  - Flash "Welcome back" message
  - Set user session
  - Redirect to dashboard based on role (lecturer/student)

- **Error**: Flash "Invalid email or password" and redirect to login

---

## Authenticated Routes

### GET `/logout`
**User Logout**
- **Authentication**: Required (decorated with @login_required)
- **Description**: Clears user session and logs out
- **Redirect**: Landing page with success message
- **Response**: Flash "You have been logged out"

---

## Lecturer Routes
*All require @login_required and @lecturer_required decorators*

### GET `/lecturer/dashboard`
**Lecturer Dashboard**
- **Authentication**: Required (Lecturer role only)
- **Template**: `lecturer_dashboard.html`
- **Description**: View and manage all uploaded notes
- **Parameters**: `page` (optional, default=1)
- **Query**: Notes.query.filter_by(uploaded_by=current_user.id)
- **Pagination**: 10 notes per page
- **Columns**: Course Code, Course Title, Filename, Upload Date, Actions
- **Actions**: Delete button for each note

---

### GET `/lecturer/upload`
**Upload Form (Display)**
- **Authentication**: Required (Lecturer role only)
- **Template**: `upload.html`
- **Description**: Form to upload new lecture note
- **Fields**: 
  - Course Title (text input)
  - Course Code (text input)
  - File (file input - PDF/DOCX)

---

### POST `/lecturer/upload`
**Upload Lecture Note (Process)**
- **Authentication**: Required (Lecturer role only)
- **Parameters**:
  - `course_title` (required): Course name
  - `course_code` (required): Course identifier
  - `file` (required): PDF/DOCX file

- **File Validation**:
  - Extension must be in ALLOWED_EXTENSIONS (pdf, docx, doc)
  - File size must be < 50 MB

- **Processing**:
  1. Secure filename using werkzeug
  2. Add timestamp prefix (YYYYMMDD_HHMMSS_)
  3. Save file to `/uploads/` directory
  4. Create Note record in database
  5. Store original filename for download

- **Success**: Flash "Lecture note uploaded successfully!" and redirect to dashboard
- **Error**: Flash specific error message and redirect to upload form
- **Database**: Creates new Note record with user_id association

---

### POST `/lecturer/delete/<note_id>`
**Delete Lecture Note**
- **Authentication**: Required (Lecturer role only)
- **Parameters**: `note_id` (integer)
- **Description**: Delete a note uploaded by current user

- **Authorization**: Verifies note was uploaded by current_user
- **File Deletion**: Removes file from `/uploads/` if exists
- **Database Deletion**: Removes Note record
- **Success**: Flash "Lecture note deleted successfully!" and redirect to dashboard
- **Error**: Flash error message if not owner

---

## Student Routes
*All require @login_required and @student_required decorators*

### GET `/student/dashboard`
**Student Dashboard**
- **Authentication**: Required (Student role only)
- **Template**: `student_dashboard.html`
- **Description**: Browse and search available lecture notes
- **Parameters**: 
  - `page` (optional, default=1): Pagination
  - `search` (optional): Search term for course code/title

- **Search Logic**:
  ```python
  WHERE course_code LIKE '%search%' 
     OR course_title LIKE '%search%'
  ```
  - Case-insensitive partial matching
  - Searches both course code and title

- **Pagination**: 10 notes per page
- **Columns**: Course Code, Course Title, Filename, Lecturer, Upload Date, Download Button
- **Sorting**: By upload_date DESC (newest first)

- **UI Elements**:
  - Search box with clear button
  - Alert showing search term if active
  - Pagination controls
  - Download button for each note

---

### GET `/student/download/<note_id>`
**Download Lecture Note**
- **Authentication**: Required (Student role only)
- **Parameters**: `note_id` (integer)
- **Description**: Download note file

- **Processing**:
  1. Fetch Note from database (404 if not found)
  2. Verify file exists on filesystem
  3. Send file as attachment
  4. Use original filename for download

- **Success**: File downloads with original filename
- **Error**: Flash error message and redirect to dashboard if file missing

- **Response Header**:
  - Content-Type: application/octet-stream
  - Content-Disposition: attachment; filename="original_name"

---

## Database Operations

### User Model
```python
class User(UserMixin, db.Model):
    id: INT (PK, AI)
    name: VARCHAR(255)
    email: VARCHAR(255) UNIQUE
    password_hash: VARCHAR(255)
    role: ENUM('lecturer', 'student')
    created_at: DATETIME
    
    Methods:
    - set_password(password) → hashes and stores
    - check_password(password) → validates
    - notes → relationship to Note table
```

### Note Model
```python
class Note(db.Model):
    id: INT (PK, AI)
    course_title: VARCHAR(255)
    course_code: VARCHAR(50)
    filename: VARCHAR(255) → original filename
    file_path: VARCHAR(500) → full path in /uploads/
    uploaded_by: INT (FK → users.id)
    upload_date: DATETIME
    
    Relationships:
    - uploader → User (backref to notes)
```

---

## Error Handling

### HTTP Status Codes
- 200: Success
- 404: Resource not found (GET requests for non-existent notes)
- 302: Redirect (after POST, unauthorized access)
- 400: Bad request (validation errors via flashing)

### Flash Messages

**Success Messages**:
- "Registration successful! You are registered as a {role}."
- "Welcome back, {name}!"
- "Lecture note uploaded successfully!"
- "Lecture note deleted successfully!"
- "You have been logged out."

**Error Messages**:
- "All fields are required."
- "Password must be at least 6 characters."
- "Passwords do not match."
- "Invalid role selected."
- "Email already registered."
- "Invalid email or password."
- "Only PDF and DOCX files are allowed."
- "You must be a lecturer/student to access this page."
- "You do not have permission to delete this note."
- "File not found."

---

## Security & Authorization

### Decorators
```python
@login_required
# Requires authentication, redirects to login if not

@lecturer_required
# Requires lecturer role, redirects to login with error if not

@student_required
# Requires student role, redirects to login with error if not
```

### Protection Examples
- Visiting `/lecturer/upload` as student → redirected to login
- Visiting `/student/dashboard` as lecturer → redirected to login
- Visiting `/lecturer/delete/<id>` without being owner → error message
- Visiting any protected route unauthenticated → redirected to login

---

## File Upload Details

### Upload Process Flow
1. User selects file and enters course details
2. Form submitted via POST to `/lecturer/upload`
3. File validation (extension, size)
4. Filename secured: `secure_filename(file.filename)`
5. Timestamp added: `{YYYYMMDD_HHMMSS_}{filename}`
6. File saved to: `uploads/{timestamped_filename}`
7. Database entry created with paths
8. Success message displayed

### Example Filenames
- Input: `Lecture Notes.pdf`
- Stored as: `uploads/20260210_143022_Lecture Notes.pdf`
- Original saved in DB: `Lecture Notes.pdf`
- Download filename: `Lecture Notes.pdf`

---

## Search & Filter

### Search in Student Dashboard
```
GET /student/dashboard?search=CS101
GET /student/dashboard?search=python&page=2
```

### Query Pattern
- Searches in both `course_code` and `course_title`
- Case-insensitive matching
- Partial matches allowed
- Example: search="cs" matches "CS101" and "Advanced CS Course"

---

## Pagination

### Pattern
All listing pages support pagination with `?page=N`

### Example URLs
```
/lecturer/dashboard          # Page 1 (default)
/lecturer/dashboard?page=2
/student/dashboard           # Page 1 (default)
/student/dashboard?page=3
/student/dashboard?search=math&page=2
```

### Implementation
- Uses Flask-SQLAlchemy pagination
- `paginate(page=page_num, per_page=10)`
- Returns: `notes.items`, `notes.pages`, `notes.has_prev`, `notes.has_next`

---

## Session Management

### Login Session
- Uses Flask-Login with UserMixin
- Session lifetime: 7 days (configurable)
- Cookies: HTTP-only for security
- User loader: `User.query.get(user_id)`

### Logout
- Calls `logout_user()` from Flask-Login
- Clears session
- Redirects to home page

---

## Configuration Parameters

### File Upload
```python
UPLOAD_FOLDER = 'uploads/'
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
```

### Security
```python
SECRET_KEY = 'dev-secret-key-change-in-production'
SESSION_COOKIE_HTTPONLY = True
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
```

### Database
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/lnsp'
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

---

## Testing Endpoints

### User Registration Flow
```bash
POST /register
Content-Type: application/x-www-form-urlencoded

name=John Doe&email=john@example.com&password=password123&confirm_password=password123&role=student
```

### User Login Flow
```bash
POST /login
Content-Type: application/x-www-form-urlencoded

email=john@example.com&password=password123
```

### File Upload Flow
```bash
POST /lecturer/upload
Content-Type: multipart/form-data

course_title=Python Basics
course_code=CS101
file=<binary PDF/DOCX file>
```

---

**API Documentation Version**: 1.0  
**Last Updated**: February 2026  
**Status**: Complete
