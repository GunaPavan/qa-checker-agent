class QAReportGenerator:
    """
    Generates the final QA validation report.
    """

    def __init__(self, report, issues, severity_summary, score, status):
        self.report = report
        self.issues = issues
        self.summary = severity_summary
        self.score = score
        self.status = status

    def generate(self):

        print("\n")
        print("=" * 40)
        print("QA VALIDATION REPORT")
        print("=" * 40)

        print(f"Report ID: {self.report.get('report_id')}")
        print(f"Entity: {self.report.get('entity')}")
        print(f"Report Type: {self.report.get('report_type')}")
        print(f"Date: {self.report.get('report_date')}")

        print("\nIssues Found:")

        if not self.issues:
            print("None")
        else:
            for i, issue in enumerate(self.issues, start=1):
                print(
                    f"{i}. [{issue['severity']}] {issue['issue_type']} - {issue['description']}"
                )

        print("\nIssue Severity Summary:")
        print(self.summary)

        print("\nQuality Score:", self.score, "/ 100")
        print("Status:", self.status)

        print("=" * 40)
