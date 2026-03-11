import psycopg2
import os
import json


class ReportDatabase:

    def __init__(self):
        self.conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        self.conn.autocommit = True

    def report_exists(self, report):
        """
        Check if the same report already exists
        """

        cursor = self.conn.cursor()

        query = """
        SELECT 1
        FROM reports
        WHERE entity = %s
        AND report_type = %s
        AND report_date = %s
        LIMIT 1
        """

        cursor.execute(
            query,
            (
                report["entity"],
                report["report_type"],
                report["report_date"]
            )
        )

        exists = cursor.fetchone() is not None
        cursor.close()

        return exists

    def insert_report(self, report):
        """
        Store report only if it does not already exist
        """

        if self.report_exists(report):
            return False

        cursor = self.conn.cursor()

        query = """
        INSERT INTO reports (entity, report_type, report_date, report_json)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                report["entity"],
                report["report_type"],
                report["report_date"],
                json.dumps(report)
            )
        )

        cursor.close()

        return True

    def get_previous_reports(self, entity, report_type, report_date):
        """
        Fetch ALL previous reports for historical comparison
        """

        cursor = self.conn.cursor()

        query = """
        SELECT report_json
        FROM reports
        WHERE entity = %s
        AND report_type = %s
        AND report_date < %s
        ORDER BY report_date DESC
        """

        cursor.execute(query, (entity, report_type, report_date))

        rows = cursor.fetchall()
        cursor.close()

        return [row[0] for row in rows]