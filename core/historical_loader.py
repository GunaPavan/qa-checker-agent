from core.database import ReportDatabase


class HistoricalLoader:
    """
    Loads all previous reports for historical comparison.
    """

    def __init__(self, report):
        self.report = report
        self.db = ReportDatabase()

    def load_previous_reports(self):

        entity = self.report.get("entity")
        report_type = self.report.get("report_type")
        report_date = self.report.get("report_date")

        previous_reports = self.db.get_previous_reports(
            entity,
            report_type,
            report_date
        )

        return previous_reports