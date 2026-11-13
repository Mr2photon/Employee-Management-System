
import sqlite3
from pathlib import Path


# Project directory
BASE_DIR = Path(__file__).resolve().parent

# Database directory
DATABASE_DIR = BASE_DIR / "instance"

# Database file
DATABASE_PATH = DATABASE_DIR / "employees.db"


def get_db_connection():
    """
    Establish connection with SQLite database.
    """

    # Create instance directory if it doesn't exist
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    # Establish database connection
    connection = sqlite3.connect(DATABASE_PATH)

    # Return rows as dictionary-like objects
    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    """
    Initialize database and create employees table.
    """

    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS employees (

            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,

            employee_code TEXT NOT NULL UNIQUE,

            first_name TEXT NOT NULL,

            last_name TEXT NOT NULL,

            email TEXT NOT NULL UNIQUE,

            phone TEXT,

            department TEXT NOT NULL,

            designation TEXT NOT NULL,

            salary REAL NOT NULL CHECK (salary >= 0),

            joining_date TEXT NOT NULL,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
    """)

    connection.commit()

    connection.close()

    print("Employee database initialized successfully!")


if __name__ == "__main__":
    init_db()
