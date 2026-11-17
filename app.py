import os
from flask_wtf.csrf import CSRFProtect
import sqlite3
from datetime import datetime
from math import isfinite
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort
)

from database import init_db, get_db_connection
from models import (
    add_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
    delete_employee
)


# Initialize Flask application
app = Flask(__name__)

# Development secret key.
# Set SECRET_KEY as an environment variable before production deployment.
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "dev-secret-key-emss"
)

csrf = CSRFProtect(app)
# -----------------------------------------
# Helper: Validate employee form data
# -----------------------------------------

def validate_employee_form():

    data = {
        "employee_code": request.form.get("employee_code", "").strip(),
        "first_name": request.form.get("first_name", "").strip(),
        "last_name": request.form.get("last_name", "").strip(),
        "email": request.form.get("email", "").strip().lower(),
        "phone": request.form.get("phone", "").strip(),
        "department": request.form.get("department", "").strip(),
        "designation": request.form.get("designation", "").strip(),
        "salary": request.form.get("salary", "").strip(),
        "joining_date": request.form.get("joining_date", "").strip()
    }

    required_fields = [
        "employee_code",
        "first_name",
        "last_name",
        "email",
        "department",
        "designation",
        "salary",
        "joining_date"
    ]

    for field in required_fields:
        if not data[field]:
            return None, f"{field.replace('_', ' ').title()} is required."

    if len(data["email"]) > 254 or "@" not in data["email"]:
        return None, "Please enter a valid email address."

    if len(data["employee_code"]) > 30:
        return None, "Employee code is too long."

    try:
        salary = float(data["salary"])

        if not isfinite(salary) or salary < 0:
            return None, "Salary must be a valid non-negative number."

        data["salary"] = salary

    except ValueError:
        return None, "Salary must be numeric."

    try:
        datetime.strptime(data["joining_date"], "%Y-%m-%d")
    except ValueError:
        return None, "Please enter a valid joining date."

    if len(data["phone"]) > 20:
        return None, "Phone number is too long."

    return data, None


# -----------------------------------------
# Route 1: Dashboard
# -----------------------------------------


@app.route("/")
def home():

    connection = get_db_connection()

    try:
        # 1. Total number of employees
        total_employees = connection.execute("""
            SELECT COUNT(*)
            FROM employees
        """).fetchone()[0]

        # 2. Total number of departments
        total_departments = connection.execute("""
            SELECT COUNT(DISTINCT department)
            FROM employees
        """).fetchone()[0]

        # 3. Average employee salary
        average_salary = connection.execute("""
            SELECT COALESCE(AVG(salary), 0)
            FROM employees
        """).fetchone()[0]

        # 4. Total monthly salary expense
        total_salary = connection.execute("""
            SELECT COALESCE(SUM(salary), 0)
            FROM employees
        """).fetchone()[0]

        # 5. Department-wise analytics
        department_stats = connection.execute("""
            SELECT
                department,
                COUNT(*) AS employee_count,
                ROUND(AVG(salary), 2) AS average_salary,
                ROUND(SUM(salary), 2) AS total_salary
            FROM employees
            GROUP BY department
            ORDER BY employee_count DESC
        """).fetchall()

        # 6. Recently registered employees
        recent_employees = connection.execute("""
            SELECT
                employee_id,
                employee_code,
                first_name,
                last_name,
                department,
                designation,
                joining_date
            FROM employees
            ORDER BY employee_id DESC
            LIMIT 5
        """).fetchall()

    finally:
        connection.close()

    return render_template(
        "index.html",
        total_employees=total_employees,
        total_departments=total_departments,
        average_salary=average_salary,
        total_salary=total_salary,
        department_stats=department_stats,
        recent_employees=recent_employees
    )



# -----------------------------------------
# Route 2: Display all employees
# -----------------------------------------

@app.route("/employees")
def employees():

    search_query = request.args.get("q", "").strip()

    connection = get_db_connection()

    try:
        if search_query:

            pattern = f"%{search_query}%"

            employee_list = connection.execute("""
                SELECT * FROM employees
                WHERE employee_code LIKE ?
                   OR first_name LIKE ?
                   OR last_name LIKE ?
                   OR email LIKE ?
                   OR department LIKE ?
                ORDER BY employee_id DESC
            """, (
                pattern,
                pattern,
                pattern,
                pattern,
                pattern
            )).fetchall()

        else:

            employee_list = get_all_employees()

    finally:
        connection.close()

    return render_template(
        "employees.html",
        employees=employee_list,
        search_query=search_query
    )


# -----------------------------------------
# Route 3: Add employee
# -----------------------------------------

@app.route("/add-employee", methods=["GET", "POST"])
def add_employee_route():

    if request.method == "POST":

        data, error = validate_employee_form()

        if error:
            flash(error, "danger")

            return render_template(
                "add_employee.html",
                form_data=request.form
            )

        try:
            new_id = add_employee(data)

            flash(
                f"Employee registered successfully! ID: {new_id}",
                "success"
            )

            return redirect(url_for("employees"))

        except sqlite3.IntegrityError:
            flash(
                "Employee code or email already exists.",
                "danger"
            )

        except sqlite3.Error:
            app.logger.exception("Database error while adding employee")
            flash("Unable to save employee. Please try again.", "danger")

        return render_template(
            "add_employee.html",
            form_data=request.form
        )

    return render_template("add_employee.html", form_data={})


# -----------------------------------------
# Route 4: Employee details
# -----------------------------------------

@app.route("/employee/<int:employee_id>")
def employee_details(employee_id):

    employee = get_employee_by_id(employee_id)

    if employee is None:
        abort(404)

    return render_template(
        "employee_details.html",
        employee=employee
    )


# -----------------------------------------
# Route 5: Edit employee
# -----------------------------------------

@app.route("/edit-employee/<int:employee_id>", methods=["GET", "POST"])
def edit_employee_route(employee_id):

    employee = get_employee_by_id(employee_id)

    if employee is None:
        abort(404)

    if request.method == "POST":

        data, error = validate_employee_form()

        if error:
            flash(error, "danger")

            return render_template(
                "edit_employee.html",
                employee=employee,
                form_data=request.form
            )

        try:
            updated = update_employee(employee_id, data)

            if updated:
                flash("Employee updated successfully!", "success")
            else:
                flash("No changes were saved.", "warning")

            return redirect(
                url_for(
                    "employee_details",
                    employee_id=employee_id
                )
            )

        except sqlite3.IntegrityError:
            flash(
                "Employee code or email already belongs to another employee.",
                "danger"
            )

        except sqlite3.Error:
            app.logger.exception("Database error while updating employee")
            flash("Unable to update employee. Please try again.", "danger")

        return render_template(
            "edit_employee.html",
            employee=employee,
            form_data=request.form
        )

    return render_template(
        "edit_employee.html",
        employee=employee,
        form_data=dict(employee)
    )


# -----------------------------------------
# Route 6: Delete employee
# -----------------------------------------

@app.route("/delete-employee/<int:employee_id>", methods=["POST"])
def delete_employee_route(employee_id):

    employee = get_employee_by_id(employee_id)

    if employee is None:
        abort(404)

    try:
        deleted = delete_employee(employee_id)

        if deleted:
            flash("Employee deleted successfully!", "success")
        else:
            flash("Employee could not be deleted.", "warning")

    except sqlite3.Error:
        app.logger.exception("Database error while deleting employee")
        flash("Unable to delete employee.", "danger")

    return redirect(url_for("employees"))


# -----------------------------------------
# Initialize and run application
# -----------------------------------------

if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
