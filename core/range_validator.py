class RangeValidator:
    """
    Validates numeric ranges for metrics.
    """

    def __init__(self, report: dict):
        self.report = report
        self.issues = []

    def validate(self):

        metrics = self.report.get("metrics", {})

        self._check_compliance_score(metrics)
        self._check_revenue_values(metrics)

        return self.issues

    def _check_compliance_score(self, metrics):

        score = metrics.get("compliance_score")

        if score is None:
            return

        if not (0 <= score <= 100):
            self.issues.append({
                "issue_type": "RANGE_ERROR",
                "field": "compliance_score",
                "description": f"Compliance score out of range: {score}",
                "severity": "MEDIUM"
            })

    def _check_revenue_values(self, metrics):

        total = metrics.get("total_revenue")

        if total is not None and total < 0:
            self.issues.append({
                "issue_type": "RANGE_ERROR",
                "field": "total_revenue",
                "description": "Revenue cannot be negative",
                "severity": "HIGH"
            })

        breakdown = metrics.get("revenue_breakdown", {})

        for category, value in breakdown.items():
            if value < 0:
                self.issues.append({
                    "issue_type": "RANGE_ERROR",
                    "field": category,
                    "description": f"Negative revenue detected: {value}",
                    "severity": "HIGH"
                })
