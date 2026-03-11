class QualityScorer:
    """
    Calculates overall quality score of the report
    based on detected issues.
    """

    PENALTIES = {
        "CRITICAL": 30,
        "HIGH": 20,
        "MEDIUM": 10,
        "LOW": 5
    }

    def __init__(self, issues):
        self.issues = issues

    def calculate_score(self):

        score = 100

        for issue in self.issues:

            severity = issue.get("severity", "LOW")

            penalty = self.PENALTIES.get(severity, 0)

            score -= penalty

        # Ensure score stays within 0–100
        score = max(0, min(score, 100))

        return score

    def get_status(self, score):

        if score >= 90:
            return "PASS"

        elif score >= 70:
            return "REVIEW"

        else:
            return "FAIL"
