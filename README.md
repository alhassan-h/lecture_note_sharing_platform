# Lecture Note Sharing Platform (LNSP)

A web-based platform for lecturers to share lecture notes with students. Built for flexibility—works locally with SQLite, scales to MySQL, and deploys to the cloud with PostgreSQL/Supabase.

## Project Overview

This is a full-featured web application built with Flask that allows:
- **Lecturers** to upload, manage, and organize lecture notes
- **Students** to browse, search, and download lecture notes
- **Role-based access control** ensuring proper permissions
- **Multiple database support** (SQLite, MySQL, PostgreSQL/Supabase)
- **Cloud deployment ready** (Vercel + Supabase)

## Technology Stack

- **Backend**: Python 3.8+ with Flask 3.0.0
- **Database**: SQLite (dev), MySQL (optional), PostgreSQL via Supabase (production)
- **Frontend**: HTML5, Bootstrap 5
- **Authentication**: Flask-Login
- **ORM**: SQLAlchemy
- **File Storage**: Local filesystem or Supabase Storage (cloud)
- **Deployment**: Vercel (serverless)

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Optional: MySQL Server 8.0+ (if using MySQL locally)
- Optional: Supabase account (free tier available at [supabase.com](https://supabase.com))

## Quick Start (Local Development)

### 1. Clone or set up the project

```bash
# If you haven't cloned yet
git clone <your-repo-url>
cd lnsp
```

### 2. Create a Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

The application defaults to SQLite for local development. To initialize:

```bash
python init_db.py
```

This creates a local `lnsp.db` file with all required tables.

### 5. Run the Application

```bash
python run.py
```

Visit `http://localhost:5000` in your browser.

### Default Test Credentials

Test the application with these credentials:
- **Lecturer**: `lecturer@example.com` / `password`
- **Student**: `student@example.com` / `password`

Or register new accounts!

## Database Configuration

The application supports three database options. Switch between them by setting the `DB_CONNECTION` environment variable.

### SQLite (Default - Local Development)

No additional setup needed. Uses a local `lnsp.db` file.

```bash
# In .env or environment
DB_CONNECTION=sqlite
```

### MySQL (Self-hosted or Managed)

Requires MySQL 8.0+. Set up connection in `.env`:

```bash
DB_CONNECTION=mysql
DATABASE_URL=mysql+pymysql://user:password@localhost/lnsp
```

Then initialize:
```bash
python init_db.py
```

### PostgreSQL/Supabase (Production-Ready)

Recommended for Vercel deployment. See [SUPABASE_SETUP.md](SUPABASE_SETUP.md) for detailed instructions.

```bash
DB_CONNECTION=postgres
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

## Deployment

### Deploy to Vercel (with Supabase)

The platform is configured for serverless deployment on Vercel. Follow these guides:

1. **Supabase Setup**: Read [SUPABASE_SETUP.md](SUPABASE_SETUP.md)
   - Create a free Supabase project
   - Get your database and storage credentials
   - Configure your environment variables

2. **Vercel Deployment**: Read [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)
   - Connect your GitHub repository to Vercel
   - Set environment variables in Vercel
   - Deploy in one click!

**Why Supabase + Vercel?**
- Vercel's serverless functions don't have persistent storage
- Supabase provides managed PostgreSQL + cloud storage
- Perfect combination for scalable, serverless architecture
- Free tier includes 500MB DB and 1GB storage

## Project Structure

```
lnsp/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # SQLAlchemy models (User, Note)
│   ├── supabase_client.py   # Supabase integration (new!)
│   ├── routes/
│   │   ├── auth.py          # Authentication routes
│   │   ├── lecturer.py      # Lecturer routes (upload, delete)
│   │   └── student.py       # Student routes (browse, download)
│   └── templates/           # Jinja2 HTML templates
├── config.py                # Application configuration
├── run.py                   # Entry point
├── init_db.py               # Database initialization
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── vercel.json              # Vercel deployment config
├── setup.sh                 # Automated setup (Unix/Linux/macOS)
├── setup.bat                # Automated setup (Windows)
├── SUPABASE_SETUP.md        # Supabase configuration guide
├── VERCEL_DEPLOYMENT.md     # Vercel deployment guide
└── README.md                # This file
```

## Key Features

### For Lecturers
- ✅ Secure login with role-based access
- ✅ Upload lecture notes (PDF, DOCX)
- ✅ View all uploaded notes with metadata
- ✅ Delete notes (with confirmation)
- ✅ Course organization (code + title)

### For Students
- ✅ Secure login with role-based access
- ✅ Browse all available lecture notes
- ✅ Search by course code or title
- ✅ Download lecture notes
- ✅ Pagination for large datasets

### For System Administrators
- ✅ Role-based access control (RBAC)
- ✅ Database flexibility (SQLite, MySQL, PostgreSQL)
- ✅ Environment-based configuration
- ✅ Cloud-ready deployment
- ✅ Automated setup scripts

## Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
# Database Configuration
DB_CONNECTION=sqlite              # Options: sqlite, mysql, postgres
DATABASE_URL=                      # Optional: override default connection string

# Supabase (for cloud deployment)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
SUPABASE_BUCKET_NAME=lecture-notes

# Flask Configuration
SECRET_KEY=your-secret-key        # Change in production!
FLASK_ENV=production              # development or production
```

See [SUPABASE_SETUP.md](SUPABASE_SETUP.md) for detailed environment variable setup.

## Development Workflow

### Running with Automated Setup

We provide scripts to automate the entire setup:

**On macOS/Linux/WSL:**
```bash
chmod +x setup.sh
./setup.sh
```

**On Windows:**
```cmd
.\setup.bat
```

These scripts will:
1. Create a virtual environment
2. Activate it
3. Install dependencies
4. Initialize the database
5. Start the application

### Manual Development

```bash
# Activate venv (as shown in Quick Start)

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run the application
python run.py

# Visit http://localhost:5000
```

### Making Changes

1. Make code changes
2. Database schema changes? Update `models.py` and run `python init_db.py`
3. Changes are hot-reloaded (Flask development mode)
4. Test your changes
5. Commit and push

## Testing

To test the application:

1. Start the server (`python run.py`)
2. Open http://localhost:5000
3. Register a new lecturer account
4. Upload a test PDF or DOCX file
5. Log out and register a student account
6. Search for and download the test file

## Troubleshooting

### "No module named 'app'"
Ensure you're in the correct directory and virtual environment is activated.

### "Database connection failed"
- Check `DB_CONNECTION` environment variable
- Verify MySQL/Supabase credentials in `DATABASE_URL`
- Ensure database server is running

### "Supabase authentication failed"
- Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct
- Check that API key hasn't been revoked in Supabase dashboard

### "File upload failing"
- Ensure `uploads/` directory exists (created by app)
- Check write permissions
- If using Supabase, verify bucket exists and is public

See [SUPABASE_SETUP.md](SUPABASE_SETUP.md) and [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for more troubleshooting.

## Contributing

To contribute to this project:

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Test thoroughly
4. Commit: `git commit -m "Add your feature"`
5. Push: `git push origin feature/your-feature`
6. Create a Pull Request

## License

This project is open source. Feel free to use, modify, and distribute.

## Support Resources

- **Flask Documentation**: https://flask.palletsprojects.com
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org
- **Supabase Documentation**: https://supabase.com/docs
- **Vercel Documentation**: https://vercel.com/docs
- **Bootstrap Documentation**: https://getbootstrap.com/docs

## Future Enhancements

Possible improvements:

- [ ] User email verification
- [ ] Password reset functionality
- [ ] Advanced search filters (date range, file type)
- [ ] File preview (PDF viewer)
- [ ] User ratings/reviews of notes
- [ ] Email notifications
- [ ] Admin dashboard for user management
- [ ] Audit logging
- [ ] Two-factor authentication
- [ ] File encryption at rest

---

**Ready to deploy?** Start with [SUPABASE_SETUP.md](SUPABASE_SETUP.md) → [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)

**Running locally?** Just run `python run.py` (SQLite works out of the box!)


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
