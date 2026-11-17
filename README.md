
# Employee Management System (EMS)

A web-based Employee Management System developed using Python Flask and SQLite. The application provides a centralized platform to manage employee records, including adding, viewing, updating, searching, and deleting employee information.

---

## 1. Project Overview

The Employee Management System (EMS) is designed to simplify employee record management through a user-friendly web interface.

The system allows administrators to maintain employee information, monitor department-wise records, and perform CRUD (Create, Read, Update, Delete) operations.

## 2. Project Objectives

- Develop a web-based employee management application.
- Implement CRUD operations for employee records.
- Store employee information using an SQLite database.
- Provide employee search functionality.
- Create a simple and responsive user interface.
- Apply collaborative software development practices using Git and GitHub.

## 3. Features

| Feature | Description |
|---|---|
| Dashboard | Displays employee management information and statistics |
| Employee Directory | Displays the list of employees |
| Add Employee | Adds new employee records |
| View Employee | Displays individual employee details |
| Edit Employee | Updates existing employee information |
| Delete Employee | Removes employee records |
| Search | Searches employee records |
| Error Handling | Displays custom 404 and 500 error pages |
| Responsive Navigation | Provides navigation across application pages |

## 4. Technology Stack

**Backend**
- Python
- Flask

**Database**
- SQLite

**Frontend**
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

**Development Tools**
- Git
- GitHub
- GitHub Codespaces
- Visual Studio Code

## 5. Project Structure

```text
Employee-Management-System/
│
├── app.py
├── database.py
├── models.py
├── test_database.py
├── requirements.txt
│
├── instance/
│   └── employees.db
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── images/
│   └── js/
│       └── script.js
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── employees.html
│   ├── add_employee.html
│   ├── edit_employee.html
│   ├── employee_details.html
│   ├── 404.html
│   └── 500.html
│
├── README.md
└── CONTRIBUTING.md
```

## 6. Installation and Setup

### Prerequisites

- Python 3 installed
- Git installed
- Internet connection for installing dependencies and loading Bootstrap CDN resources

### Step 1: Clone the Repository

```bash
git clone https://github.com/Mr2photon/Employee-Management-System.git
```

### Step 2: Open the Project Directory

```bash
cd Employee-Management-System
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate the Virtual Environment

**Linux / Ubuntu / macOS**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
python app.py
```

### Step 7: Open in Browser

Visit:

```text
http://127.0.0.1:5000
```

The application initializes its SQLite database when started.

## 7. Database

The project uses SQLite for storing employee information.

The database operations are organized through:

- `database.py` — database initialization and connection.
- `models.py` — employee database operations.
- `test_database.py` — database operation testing.

## 8. Application Pages

1. Dashboard
2. Employee Directory
3. Add Employee
4. Employee Details
5. Edit Employee
6. Custom 404 Error Page
7. Custom 500 Error Page

## 9. Team Contributions

This project is developed collaboratively by two team members.

| Member | Responsibilities |
|---|---|
| Member 1 | Backend implementation, database operations, employee CRUD functionality, dashboard analytics and security |
| Member 2 | Custom error pages, Flask error handling, navigation improvements, footer, project documentation and GitHub collaboration |

## 10. Version Control and Collaboration

Git and GitHub are used for collaborative development.

The project workflow includes:

- Separate feature branches.
- Meaningful Git commits.
- Pushing changes to GitHub.
- Creating pull requests.
- Code review.
- Merge conflict demonstration and resolution.

## 11. Future Enhancements

- User authentication and role-based access.
- Employee profile image upload.
- Export employee data to CSV or PDF.
- Advanced filtering and reporting.
- Improved security and deployment configuration.

## 12. Project Information

**Project Name:** Employee Management System

**Course:** MCA

**Academic Year:** 2026

**Backend:** Python Flask

**Database:** SQLite

**Repository:** [GitHub Repository](https://github.com/Mr2photon/Employee-Management-System)

---

*Developed as an academic project to demonstrate web application development, database management, and collaborative software development using Git and GitHub.*
