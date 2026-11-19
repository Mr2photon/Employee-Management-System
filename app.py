import csv
import io
from flask import request
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
    abort,
    Response
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




def validate_employee_form(form_data=None):

    if form_data is None:

        form_data = request.form

    data = {
        "employee_code": (form_data.get("employee_code") or "").strip(),
        "first_name": (form_data.get("first_name") or "").strip(),
        "last_name": (form_data.get("last_name") or "").strip(),
        "email": (form_data.get("email") or "").strip().lower(),
        "phone": (form_data.get("phone") or "").strip(),
        "department": (form_data.get("department") or "").strip(),
        "designation": (form_data.get("designation") or "").strip(),
        "salary": (form_data.get("salary") or "").strip(),
        "joining_date": (form_data.get("joining_date") or "").strip()
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
# Route: Export employees to CSV
# -----------------------------------------

@app.route("/export-employees")
def export_employees():

    search_query = request.args.get("q", "").strip()

    # Retrieve employees using the same search logic
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
            """, (pattern, pattern, pattern, pattern, pattern)).fetchall()

        else:
            employee_list = get_all_employees()

    finally:
        connection.close()

    # Create CSV content in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # CSV column headings
    writer.writerow([
        "Employee ID",
        "Employee Code",
        "First Name",
        "Last Name",
        "Email",
        "Phone",
        "Department",
        "Designation",
        "Salary",
        "Joining Date"
    ])

    # Write employee records
    for emp in employee_list:
        writer.writerow([
            emp["employee_id"],
            emp["employee_code"],
            emp["first_name"],
            emp["last_name"],
            emp["email"],
            emp["phone"],
            emp["department"],
            emp["designation"],
            emp["salary"],
            emp["joining_date"]
        ])

    # Return CSV as a downloadable file
    response = Response(
        output.getvalue(),
        mimetype="text/csv"
    )

    response.headers["Content-Disposition"] = (
        "attachment; filename=employees.csv"
    )

    return response


# -----------------------------------------
# Route: Import employees
# -----------------------------------------

@app.route("/import-employees", methods=["GET", "POST"])
def import_employees():

    return render_template("import_employees.html")
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
# Error Handling
# -----------------------------------------

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500


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
