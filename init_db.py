"""Database initialization script

This script supports both SQLite and MySQL. It will:
- For SQLite: create the SQLite database file and run SQLAlchemy `create_all()` to create tables.
- For MySQL: connect to the MySQL server, create the database if it doesn't exist, then run SQLAlchemy `create_all()`.

It reads the application's `SQLALCHEMY_DATABASE_URI` from `config.Config`, so you can switch databases by updating `config.py` or setting the `DATABASE_URL` environment variable.
"""
from urllib.parse import urlparse
import os
import sys
from app import create_app, db
from config import Config


def is_mysql_uri(uri: str) -> bool:
    return uri.startswith('mysql')


def parse_mysql_uri(uri: str):
    # Expect format: dialect+driver://user:password@host[:port]/dbname
    # Use urlparse to extract components
    parsed = urlparse(uri)
    username = parsed.username or 'root'
    password = parsed.password or ''
    hostname = parsed.hostname or 'localhost'
    port = parsed.port or 3306
    # path begins with '/dbname'
    dbname = parsed.path.lstrip('/') if parsed.path else 'lnsp'
    return username, password, hostname, port, dbname


def create_mysql_database(uri: str):
    try:
        import mysql.connector
    except ImportError:
        print('mysql-connector-python is required to initialize MySQL. Install it in your venv.')
        sys.exit(1)

    user, password, host, port, dbname = parse_mysql_uri(uri)

    try:
        conn = mysql.connector.connect(host=host, user=user, password=password, port=port)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}`")
        conn.commit()
        print(f"✓ Database '{dbname}' created or already exists on {host}:{port}")
    except mysql.connector.Error as e:
        print('Error creating database:', e)
        sys.exit(1)
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


def main():
    print('Initializing database for LNSP...')

    # Allow overriding the SQLALCHEMY_DATABASE_URI via env var DATABASE_URL
    database_uri = os.environ.get('DATABASE_URL') or Config.SQLALCHEMY_DATABASE_URI

    # Create Flask app (this will initialize extensions but not create tables)
    app = create_app('config.Config')

    if is_mysql_uri(database_uri):
        print('Detected MySQL URI — ensuring database exists...')
        create_mysql_database(database_uri)

    # Create tables using SQLAlchemy
    with app.app_context():
        print('Creating tables via SQLAlchemy...')
        db.create_all()
        print('✓ Tables created (if not present).')


if __name__ == '__main__':
    main()
