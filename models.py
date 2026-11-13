
from database import get_db_connection


def add_employee(data):
    """
    Insert a new employee into the database.
    """

    connection = get_db_connection()

    try:
        cursor = connection.execute("""
            INSERT INTO employees (
                employee_code,
                first_name,
                last_name,
                email,
                phone,
                department,
                designation,
                salary,
                joining_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["employee_code"],
            data["first_name"],
            data["last_name"],
            data["email"],
            data.get("phone"),
            data["department"],
            data["designation"],
            data["salary"],
            data["joining_date"]
        ))

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def get_all_employees():
    """
    Retrieve all employees.
    """

    connection = get_db_connection()

    try:
        employees = connection.execute("""
            SELECT * FROM employees
            ORDER BY employee_id DESC
        """).fetchall()

        return employees

    finally:
        connection.close()


def get_employee_by_id(employee_id):
    """
    Retrieve an employee using employee ID.
    """

    connection = get_db_connection()

    try:
        employee = connection.execute("""
            SELECT * FROM employees
            WHERE employee_id = ?
        """, (employee_id,)).fetchone()

        return employee

    finally:
        connection.close()


def update_employee(employee_id, data):
    """
    Update existing employee information.
    """

    connection = get_db_connection()

    try:
        cursor = connection.execute("""
            UPDATE employees
            SET
                employee_code = ?,
                first_name = ?,
                last_name = ?,
                email = ?,
                phone = ?,
                department = ?,
                designation = ?,
                salary = ?,
                joining_date = ?

            WHERE employee_id = ?
        """, (
            data["employee_code"],
            data["first_name"],
            data["last_name"],
            data["email"],
            data.get("phone"),
            data["department"],
            data["designation"],
            data["salary"],
            data["joining_date"],
            employee_id
        ))

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


def delete_employee(employee_id):
    """
    Delete an employee using employee ID.
    """

    connection = get_db_connection()

    try:
        cursor = connection.execute("""
            DELETE FROM employees
            WHERE employee_id = ?
        """, (employee_id,))

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()
