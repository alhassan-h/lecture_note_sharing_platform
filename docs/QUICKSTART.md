# Quick Start Guide

## Prerequisites
- Python 3.8+
- MySQL Server running

## Quick Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_db.py
```

### 3. Run Application
```bash
python run.py
```

Visit: http://localhost:5000

## Test the System

### Create Test Accounts

**Student Account:**
- Email: student@example.com
- Password: password123
- Role: Student

**Lecturer Account:**
- Email: lecturer@example.com
- Password: password123
- Role: Lecturer

### Test Workflow

1. **As Lecturer:**
   - Register or login
   - Upload a test PDF/DOCX with course details
   - View dashboard with uploaded notes
   - Try deleting a note

2. **As Student:**
   - Register or login
   - View available notes
   - Search by course code
   - Download a note

## Troubleshooting

**MySQL Connection Error?**
- Check `config.py` for correct credentials
- Ensure MySQL is running

**Can't upload file?**
- Check file format (PDF, DOCX only)
- Verify file size < 50 MB
- Ensure `/uploads/` directory exists

**Database not found?**
- Run `python init_db.py` again
- Check MySQL user permissions

## Project Files Checklist

- ✓ app/__init__.py (App factory)
- ✓ app/models.py (Database models)
- ✓ app/routes/auth.py (Authentication)
- ✓ app/routes/lecturer.py (Lecturer features)
- ✓ app/routes/student.py (Student features)
- ✓ app/templates/ (All HTML templates)
- ✓ config.py (Configuration)
- ✓ run.py (Entry point)
- ✓ init_db.py (Database setup)
- ✓ requirements.txt (Dependencies)
- ✓ uploads/ (File storage)

## Key Features Implemented

✓ User Authentication (Register/Login/Logout)
✓ Role-based Access Control (Lecturer/Student)
✓ File Upload (PDF/DOCX with metadata)
✓ File Download (Secure access for students)
✓ Note Management (Lecturer can upload/delete)
✓ Search & Filter (Students can search by course)
✓ Pagination (For large note lists)
✓ Bootstrap 5 UI (Responsive design)
✓ Password Security (Hashing with Werkzeug)
✓ Protected Routes (Login required)

## Development Tips

1. **Debug Mode**: Set `debug=True` in `run.py` for auto-reload
2. **Database Reset**: Delete rows manually or recreate database with `init_db.py`
3. **File Storage**: Check `/uploads/` folder for uploaded files
4. **Session**: Default 7-day session lifetime

Enjoy the platform! 📚
