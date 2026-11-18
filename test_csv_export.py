
import csv
import io
import unittest

from app import app
from database import init_db, get_db_connection


class CSVExportTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_csv_download_response(self):
        response = self.client.get("/export-employees")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/csv")
        self.assertIn(
            "attachment; filename=employees.csv",
            response.headers["Content-Disposition"]
        )

    def test_csv_column_headings(self):
        response = self.client.get("/export-employees")

        content = response.get_data(as_text=True)
        reader = csv.reader(io.StringIO(content))
        headings = next(reader)

        expected_headings = [
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
        ]

        self.assertEqual(headings, expected_headings)

    def test_csv_contains_employee_records(self):
        connection = get_db_connection()

        try:
            employee = connection.execute(
                "SELECT * FROM employees LIMIT 1"
            ).fetchone()
        finally:
            connection.close()

        if employee is None:
            self.skipTest("No employee records available for testing")

        response = self.client.get("/export-employees")

        content = response.get_data(as_text=True)
        rows = list(csv.reader(io.StringIO(content)))

        employee_codes = [row[1] for row in rows[1:]]

        self.assertIn(employee["employee_code"], employee_codes)

    def test_csv_search_filter(self):
        connection = get_db_connection()

        try:
            employee = connection.execute(
                "SELECT * FROM employees LIMIT 1"
            ).fetchone()
        finally:
            connection.close()

        if employee is None:
            self.skipTest("No employee records available for testing")

        response = self.client.get(
            "/export-employees",
            query_string={"q": employee["employee_code"]}
        )

        content = response.get_data(as_text=True)
        rows = list(csv.reader(io.StringIO(content)))

        employee_codes = [row[1] for row in rows[1:]]

        self.assertTrue(employee_codes)
        self.assertEqual(
            employee_codes,
            [employee["employee_code"]]
        )


if __name__ == "__main__":
    unittest.main()
