class IssueManager:
    """
    Collects and manages all detected issues.
    """

    def __init__(self):
        self.issues = []

    def add_issues(self, new_issues):

        if not new_issues:
            return

        self.issues.extend(new_issues)

    def get_all_issues(self):
        return self.issues

    def count_by_severity(self):

        counts = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }

        for issue in self.issues:
            severity = issue.get("severity", "LOW")

            if severity in counts:
                counts[severity] += 1

        return counts
