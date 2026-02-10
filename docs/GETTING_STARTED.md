# 🚀 LNSP Getting Started Checklist

## Pre-Installation ✓

- [ ] You have Python 3.8 or higher installed
  ```bash
  python --version
  ```

- [ ] You have MySQL Server installed and running
  ```bash
  mysql --version
  # MySQL should be running as a service
  ```

- [ ] You have pip installed
  ```bash
  pip --version
  ```

- [ ] You have this project folder: `c:\Users\alhassanh\Documents\projects\lnsp`

---

## Installation Steps ✓

### Step 1: Install Python Dependencies (2 minutes)
```bash
cd c:\Users\alhassanh\Documents\projects\lnsp
pip install -r requirements.txt
```

**Expected output**: Successfully installed Flask, SQLAlchemy, Flask-Login, etc.

### Step 2: Initialize Database (1 minute)
```bash
python init_db.py
```

**Expected output**:
```
Setting up LNSP Database...
✓ Database 'lnsp' created/exists
✓ Users table created/exists
✓ Notes table created/exists
✓ Database setup completed successfully!
```

**If error occurs**: Check that MySQL is running and credentials in `config.py` are correct

### Step 3: Start the Application (30 seconds)
```bash
python run.py
```

**Expected output**:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

**Note**: The server will run in the foreground. Don't close this terminal.

### Step 4: Open in Browser (30 seconds)
Open your web browser and go to: **http://localhost:5000**

You should see the landing page with login and register buttons.

---

## Quick Test Workflow ✓

### Test 1: Register as Student (2 minutes)
1. Click **Register** button
2. Fill in the form:
   - Full Name: `John Student`
   - Email: `student@example.com`
   - Password: `password123`
   - Confirm Password: `password123`
   - Role: **Student**
3. Click **Register** button
4. You should see: "Registration successful!"
5. Click **Login**

### Test 2: Register as Lecturer (2 minutes)
1. Click **Register** button
2. Fill in the form:
   - Full Name: `Jane Lecturer`
   - Email: `lecturer@example.com`
   - Password: `password123`
   - Confirm Password: `password123`
   - Role: **Lecturer**
3. Click **Register** button
4. You should see: "Registration successful!"

### Test 3: Login as Lecturer (2 minutes)
1. Click **Login** button
2. Enter:
   - Email: `lecturer@example.com`
   - Password: `password123`
3. Click **Login**
4. You should be redirected to **Lecturer Dashboard**
5. You should see "Upload New Note" button

### Test 4: Upload a Note (3 minutes)
1. Click **Upload New Note**
2. Fill in:
   - Course Title: `Introduction to Python`
   - Course Code: `CS101`
   - File: Create a test PDF or DOC file and select it
     - (Supported: PDF, DOCX, DOC only)
3. Click **Upload Note**
4. You should see: "Lecture note uploaded successfully!"
5. You should see the note in your dashboard

### Test 5: Login as Student (2 minutes)
1. Logout (click username/Logout)
2. Go to Login
3. Enter:
   - Email: `student@example.com`
   - Password: `password123`
4. Click **Login**
5. You should be redirected to **Student Dashboard**
6. You should see the note uploaded by lecturer

### Test 6: Download Note (1 minute)
1. In Student Dashboard, find the note
2. Click **⬇ Download** button
3. File should download to your computer
4. Check that filename is original (not timestamped)

### Test 7: Search Notes (1 minute)
1. In search box, type: `CS101`
2. Click **Search**
3. Results should show only notes with "CS101"
4. Click **Clear** to reset

---

## Verification ✓

After completing the above, verify:

- [ ] Application runs without errors
- [ ] Landing page displays correctly
- [ ] Can register as student
- [ ] Can register as lecturer
- [ ] Can login with correct credentials
- [ ] Cannot login with wrong credentials
- [ ] Lecturer dashboard shows upload form
- [ ] Student dashboard shows available notes
- [ ] Can upload a file successfully
- [ ] Can download a file successfully
- [ ] Can search notes by course code
- [ ] Can delete own notes (as lecturer)
- [ ] Student cannot see delete button
- [ ] Logout works correctly

**All items checked?** ✅ **SYSTEM IS WORKING CORRECTLY!**

---

## Troubleshooting ✓

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution**: Run `pip install -r requirements.txt` again

### Issue: "Connection refused" or database error
**Solution**: 
- Check MySQL is running: `mysql -u root -p`
- Update credentials in `config.py` if needed
- Run `python init_db.py` again

### Issue: Port 5000 already in use
**Solution**: 
- Edit `run.py` and change port number
- Or stop other applications using port 5000

### Issue: Can't upload files
**Solution**:
- File must be PDF, DOCX, or DOC
- File must be smaller than 50 MB
- Check `/uploads/` folder exists and is writable

### Issue: File won't download
**Solution**:
- Check file still exists in `/uploads/` folder
- Try logging in again
- Clear browser cache

---

## File Organization ✓

Your project should have this structure:

```
lnsp/
├── app/                    ✓
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── lecturer.py
│   │   └── student.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── upload.html
│   │   ├── lecturer_dashboard.html
│   │   └── student_dashboard.html
│   └── static/            ✓
├── uploads/               ✓ (should contain uploaded files)
├── config.py             ✓
├── run.py                ✓
├── init_db.py            ✓
├── requirements.txt      ✓
└── README.md             ✓
```

All files listed should exist.

---

## Configuration ✓

If you need to change settings:

**File**: `config.py`

```python
# MySQL connection (change if needed)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/lnsp'

# Change these for production
SECRET_KEY = 'dev-secret-key-change-in-production'

# File upload settings
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB max
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
```

---

## Next Steps ✓

After verifying everything works:

1. **Read Full Documentation**: See `README.md`
2. **Understand the API**: See `API_DOCUMENTATION.md`
3. **Review Code**: Check `app/routes/` files
4. **Customize**: Modify templates or add features
5. **Deploy**: Follow deployment guide (if needed)

---

## Database Check ✓

To verify database was set up correctly:

```bash
# Connect to MySQL
mysql -u root -p

# Enter password when prompted

# Use the LNSP database
USE lnsp;

# Check tables
SHOW TABLES;

# You should see:
# - notes
# - users

# Exit
EXIT;
```

---

## Important Files to Know ✓

| File | Purpose | Can Edit? |
|------|---------|-----------|
| `run.py` | Start application | Yes |
| `config.py` | Configuration | Yes |
| `app/models.py` | Database models | No* |
| `app/routes/` | Application logic | Yes |
| `app/templates/` | HTML pages | Yes |
| `requirements.txt` | Dependencies | Careful |
| `init_db.py` | Database setup | No |

*Can edit after understanding SQLAlchemy

---

## Common Customizations ✓

### Change Port Number
Edit `run.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Change 5000 to 8000
```

### Change Session Timeout
Edit `config.py`:
```python
PERMANENT_SESSION_LIFETIME = timedelta(days=7)  # Change 7 to desired days
```

### Change Max File Size
Edit `config.py`:
```python
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # Change to 100 MB
```

---

## When You're Done ✓

To stop the application:
1. Press **Ctrl+C** in the terminal where `python run.py` is running
2. Terminal will show: `^C` and return to prompt

To start again:
1. Open terminal in project folder
2. Run: `python run.py`

---

## Support ✓

Need help?

1. **Quick Setup**: See `QUICKSTART.md`
2. **Full Guide**: See `README.md`
3. **API Details**: See `API_DOCUMENTATION.md`
4. **Check Requirements**: See `VERIFICATION.md`

---

## Success Indicators ✓

You'll know everything is working when:

✅ Landing page loads without errors  
✅ Can register new users  
✅ Can login successfully  
✅ Lecturer can upload files  
✅ Student can see all notes  
✅ Student can search notes  
✅ Student can download files  
✅ Logout works  
✅ No error messages in browser or terminal  

---

## Final Checklist ✓

Before calling it complete:

- [ ] Project folder exists
- [ ] Python 3.8+ installed
- [ ] MySQL Server running
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database initialized (`python init_db.py`)
- [ ] Application started (`python run.py`)
- [ ] Landing page loads (http://localhost:5000)
- [ ] Can register users
- [ ] Can login successfully
- [ ] All features working

**All checked?** 🎉 **YOU'RE ALL SET!**

---

## Quick Reference Commands ✓

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Start application
python run.py

# Connect to MySQL
mysql -u root -p

# Check database
mysql -u root -p -e "USE lnsp; SHOW TABLES;"
```

---

**Document Version**: 1.0  
**Last Updated**: February 10, 2026  
**Status**: Ready to Use

---

**Congratulations!** You have a fully functional Lecture Note Sharing Platform! 🎓
