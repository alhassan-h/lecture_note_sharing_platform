"""
Database initialization script
Run this to set up the MySQL database for the LNSP
"""
import mysql.connector
from mysql.connector import Error

def create_database():
    """Create the LNSP database and tables"""
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root'
        )
        
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS lnsp")
        print("✓ Database 'lnsp' created/exists")
        
        # Use the database
        cursor.execute("USE lnsp")
        
        # Create users table
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role ENUM('lecturer', 'student') DEFAULT 'student',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX(email)
        )
        """
        cursor.execute(create_users_table)
        print("✓ Users table created/exists")
        
        # Create notes table
        create_notes_table = """
        CREATE TABLE IF NOT EXISTS notes (
            id INT PRIMARY KEY AUTO_INCREMENT,
            course_title VARCHAR(255) NOT NULL,
            course_code VARCHAR(50) NOT NULL,
            filename VARCHAR(255) NOT NULL,
            file_path VARCHAR(500) NOT NULL,
            uploaded_by INT NOT NULL,
            upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (uploaded_by) REFERENCES users(id) ON DELETE CASCADE
        )
        """
        cursor.execute(create_notes_table)
        print("✓ Notes table created/exists")
        
        connection.commit()
        print("\n✓ Database setup completed successfully!")
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    print("Setting up LNSP Database...")
    create_database()
