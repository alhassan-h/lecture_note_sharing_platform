import os
from datetime import timedelta

# Determine DB connection strategy:
# - If environment variable DB_CONNECTION is set to 'mysql', the app will use DATABASE_URL
#   or fall back to a MySQL default. Otherwise it will use SQLite by default.

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration"""
    DB_CONNECTION = os.environ.get('DB_CONNECTION', 'sqlite').lower()
    # Allow explicit DATABASE_URL override. If not provided, build a sensible default.
    DATABASE_URL = os.environ.get('DATABASE_URL')

    if DB_CONNECTION == 'mysql':
        # Prefer explicit DATABASE_URL if supplied, otherwise fall back to local MySQL default.
        SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'mysql+pymysql://root:root@localhost/lnsp'
    else:
        # Default to a local SQLite file in the project directory. Use DATABASE_URL if provided.
        SQLALCHEMY_DATABASE_URI = DATABASE_URL or f'sqlite:///{os.path.join(basedir, "lnsp.db")} '

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
