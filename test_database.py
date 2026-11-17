
from database import init_db
from models import (
    add_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
    delete_employee
)

# Step 1: Initialize database
init_db()

# Step 2: Create sample employee
employee = {
    "employee_code": "TEST001",
    "first_name": "Rahul",
    "last_name": "Sharma",
    "email": "rahul.test@example.com",
    "phone": "9876543210",
    "department": "IT",
    "designation": "Software Developer",
    "salary": 45000,
    "joining_date": "2026-01-15"
}

# Step 3: Insert employee
employee_id = add_employee(employee)

print("Inserted Employee ID:", employee_id)

# Step 4: Retrieve all employees
employees = get_all_employees()

print("\nAll Employees:")

for emp in employees:
    print(dict(emp))

# Step 5: Retrieve one employee
result = get_employee_by_id(employee_id)

print("\nIndividual Employee:")
print(dict(result) if result else "Not found")

# Step 6: Update employee
employee["department"] = "Finance"

updated = update_employee(employee_id, employee)

print("\nUpdated:", updated)

# Step 7: Delete employee
deleted = delete_employee(employee_id)

print("Deleted:", deleted)
