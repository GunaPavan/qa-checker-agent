class CalculationValidator:
    """
    Validates calculations inside the report.
    Example: revenue totals must match subcategories.
    """

    def __init__(self, report: dict):
        self.report = report
        self.issues = []

    def validate(self):

        metrics = self.report.get("metrics", {})

        total_revenue = metrics.get("total_revenue")
        breakdown = metrics.get("revenue_breakdown", {})

        if total_revenue is None or not breakdown:
            return self.issues

        calculated_sum = sum(breakdown.values())

        if calculated_sum != total_revenue:
            self.issues.append({
                "issue_type": "CALCULATION_ERROR",
                "field": "total_revenue",
                "description": f"Total revenue mismatch: expected {calculated_sum}, reported {total_revenue}",
                "severity": "HIGH"
            })

        return self.issues
