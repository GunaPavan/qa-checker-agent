class AnomalyDetector:
    """
    Detects abnormal metric changes between
    the current report and all previous reports.
    """

    WARNING_THRESHOLD = 30
    CRITICAL_THRESHOLD = 50

    def __init__(self, current_report, previous_reports):
        self.current = current_report
        self.previous_reports = previous_reports or []
        self.issues = []

    def detect(self):

        if not self.previous_reports:
            return self.issues

        current_metrics = self.current.get("metrics", {})

        # Track already flagged metrics to avoid duplicate issues
        flagged_metrics = set()

        for previous in self.previous_reports:

            previous_metrics = previous.get("metrics", {})

            for metric in current_metrics:

                if metric in flagged_metrics:
                    continue

                if metric not in previous_metrics:
                    continue

                current_value = current_metrics[metric]
                previous_value = previous_metrics[metric]

                if not isinstance(current_value, (int, float)):
                    continue

                if not isinstance(previous_value, (int, float)):
                    continue

                if previous_value == 0:
                    continue

                change = ((current_value - previous_value) / previous_value) * 100

                severity = None

                if abs(change) > self.CRITICAL_THRESHOLD:
                    severity = "CRITICAL"

                elif abs(change) > self.WARNING_THRESHOLD:
                    severity = "WARNING"

                if severity:
                    self.issues.append({
                        "issue_type": "ANOMALY_DETECTED",
                        "field": metric,
                        "description": f"{metric} changed by {change:.2f}% compared to previous report",
                        "severity": severity
                    })

                    flagged_metrics.add(metric)

        return self.issues