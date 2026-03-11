class SchemaValidator:
    """
    Validates the structure of the report before further analysis.
    """

    REQUIRED_FIELDS = [
        "report_id",
        "report_type",
        "entity",
        "report_date",
        "metrics"
    ]

    REQUIRED_METRICS = [
        "total_revenue",
        "revenue_breakdown",
        "compliance_score"
    ]

    def __init__(self, report: dict):
        self.report = report
        self.issues = []

    def validate(self):
        """
        Run all schema validation checks.
        """
        self._check_required_fields()
        self._check_metrics_structure()

        return self.issues

    def _check_required_fields(self):
        """
        Ensure top-level fields exist.
        """

        for field in self.REQUIRED_FIELDS:
            if field not in self.report:
                self.issues.append({
                    "issue_type": "MISSING_FIELD",
                    "field": field,
                    "description": f"Missing required field: {field}",
                    "severity": "HIGH"
                })

    def _check_metrics_structure(self):
        """
        Ensure required metrics exist.
        """

        metrics = self.report.get("metrics")

        if not metrics:
            self.issues.append({
                "issue_type": "MISSING_DATA",
                "field": "metrics",
                "description": "Metrics section missing",
                "severity": "HIGH"
            })
            return

        for metric in self.REQUIRED_METRICS:
            if metric not in metrics:
                self.issues.append({
                    "issue_type": "MISSING_METRIC",
                    "field": metric,
                    "description": f"Missing required metric: {metric}",
                    "severity": "HIGH"
                })
