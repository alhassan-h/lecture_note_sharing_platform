# Lecture Note Sharing Platform (LNSP)

A simple web-based platform for lecturers to share lecture notes with students.

## Project Overview

This is a proof-of-concept web application built with Flask that allows:
- **Lecturers** to upload, manage, and organize lecture notes
- **Students** to browse, search, and download lecture notes
- **Role-based access control** ensuring proper permissions

## Technology Stack

- **Backend**: Python 3.8+ with Flask 3.0.0
- **Database**: MySQL 8.0+
- **Frontend**: HTML5, Bootstrap 5
- **Authentication**: Flask-Login
- **ORM**: SQLAlchemy
- **File Storage**: Local filesystem (`/uploads` directory)

## Prerequisites

- Python 3.8 or higher
- MySQL Server 8.0 or higher
- pip (Python package installer)

## Installation & Setup

### 1. Create MySQL Database

First, ensure MySQL is running and execute:

```bash
python init_db.py
```

This will create the `lnsp` database and all required tables.

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Database Connection

Edit `config.py` and update the database URI if needed:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/lnsp'
```

Update `root:root` with your MySQL username and password.

### 4. Run the Application

```bash
python run.py
```

The application will start at `http://localhost:5000`

## Project Structure

```
lnsp/
├── app/
│   ├── __init__.py              # App factory and initialization
│   ├── models.py                # Database models (User, Note)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication routes
│   │   ├── lecturer.py          # Lecturer routes
│   │   └── student.py           # Student routes
│   ├── templates/
│   │   ├── base.html            # Base template
│   │   ├── index.html           # Landing page
│   │   ├── login.html           # Login page
│   │   ├── register.html        # Registration page
│   │   ├── upload.html          # Upload notes form
│   │   ├── lecturer_dashboard.html  # Lecturer dashboard
│   │   └── student_dashboard.html   # Student dashboard
│   └── static/                  # CSS, JS, images
├── uploads/                     # Uploaded lecture notes
├── config.py                    # Configuration settings
├── run.py                       # Application entry point
├── init_db.py                   # Database initialization script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Database Schema

### Users Table

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary Key, Auto-increment |
| name | VARCHAR(255) | User's full name |
| email | VARCHAR(255) | Unique email address |
| password_hash | VARCHAR(255) | Hashed password |
| role | ENUM | 'lecturer' or 'student' |
| created_at | DATETIME | Account creation timestamp |

### Notes Table

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary Key, Auto-increment |
| course_title | VARCHAR(255) | Course name |
| course_code | VARCHAR(50) | Course identifier |
| filename | VARCHAR(255) | Original file name |
| file_path | VARCHAR(500) | Path to stored file |
| uploaded_by | INT | Foreign Key to users.id |
| upload_date | DATETIME | Upload timestamp |

## Features

### Authentication & Authorization
- User registration with role selection
- Secure login/logout with password hashing
- Role-based access control (Lecturer/Student)
- Session management

### For Lecturers
- **Dashboard**: View all uploaded notes with pagination
- **Upload**: Upload PDF/DOCX files with course details
- **Manage**: Delete outdated or incorrect notes
- **Organization**: Organize by course code and title

### For Students
- **Dashboard**: View all available lecture notes
- **Search**: Filter notes by course code or title
- **Download**: Download notes in original format
- **Browse**: Browse by lecturer

### UI/UX
- Clean, academic-focused design
- Responsive Bootstrap 5 layout
- Mobile-friendly interface
- Flash messages for user feedback
- Pagination for large lists

## Security Features

- Password hashing using Werkzeug
- Protected routes with login required decorator
- Role-based access control decorators
- File type validation (PDF, DOCX only)
- CSRF protection via Flask-Login
- Session cookie HTTP-only flag
- Secure filename handling

## File Upload

- **Supported Formats**: PDF, DOCX, DOC
- **Max File Size**: 50 MB
- **Storage**: `/uploads/` directory with timestamped names
- **Permissions**: Only lecturers can upload; only authenticated users can download

## Usage Guide

### For Students

1. Go to `http://localhost:5000`
2. Click "Register" and select "Student" role
3. Fill in your details and create account
4. Log in with your credentials
5. Browse available lecture notes
6. Search by course code or title
7. Click "Download" to get the file

### For Lecturers

1. Go to `http://localhost:5000`
2. Click "Register" and select "Lecturer" role
3. Fill in your details and create account
4. Log in with your credentials
5. Click "Upload Note" to add lecture materials
6. Fill in course code, title, and select file
7. Click "Upload Note" to save
8. Manage notes from your dashboard
9. Delete notes using the delete button if needed

## API Endpoints

### Authentication Routes
- `GET /` - Landing page
- `GET /register` - Registration form
- `POST /register` - Register new user
- `GET /login` - Login form
- `POST /login` - Authenticate user
- `GET /logout` - Logout user (requires authentication)

### Lecturer Routes
- `GET /lecturer/dashboard` - View all uploaded notes
- `GET /lecturer/upload` - Upload form
- `POST /lecturer/upload` - Upload new note
- `POST /lecturer/delete/<id>` - Delete note

### Student Routes
- `GET /student/dashboard` - View all available notes with search
- `GET /student/download/<id>` - Download note file

## Configuration

### Environment Variables (if needed)

```bash
FLASK_ENV=development      # or production
FLASK_DEBUG=True          # or False
SECRET_KEY=your-secret    # Set a strong secret key
DATABASE_URL=mysql://...  # Database connection string
```

## Error Handling

The application includes error handling for:
- Missing or invalid form inputs
- Duplicate email registration
- Invalid login credentials
- Unauthorized access attempts
- Missing or deleted files
- File upload errors

## Limitations & Out of Scope

As per the content brief, the following are NOT implemented:
- Real-time chat or messaging
- Email notifications
- Grading system
- Email verification
- Cloud storage (local filesystem only)
- Admin management interface
- Advanced reporting

## Troubleshooting

### Database Connection Error
- Ensure MySQL service is running
- Verify credentials in `config.py`
- Check database exists: `mysql -u root -p -e "SHOW DATABASES;"`

### File Upload Fails
- Check `/uploads/` folder has write permissions
- Verify file is in supported format (PDF, DOCX)
- Ensure file size is under 50 MB

### Import Errors
- Run `pip install -r requirements.txt` again
- Ensure Python 3.8+ is being used

## Future Enhancements

Potential improvements for production version:
- Cloud storage integration (AWS S3, Google Drive)
- Email notifications
- Course management system
- User profile pages
- Advanced search/filtering
- Note ratings and comments
- Bulk upload functionality
- PDF preview in browser

## License

This is a demonstration/educational project.

## Support

For issues or questions, refer to the original content brief: `Lecture_Note_Sharing_Platform_Content_Brief.md`
