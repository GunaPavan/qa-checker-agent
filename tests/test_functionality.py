import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.parser import ReportParser
from core.schema_validator import SchemaValidator
from core.calculation_validator import CalculationValidator
from core.range_validator import RangeValidator
from core.historical_loader import HistoricalLoader
from core.anomaly_detector import AnomalyDetector
from core.issue_manager import IssueManager
from core.quality_scorer import QualityScorer
from core.database import ReportDatabase
from output.qa_report_generator import QAReportGenerator


file_path = "data/reports/report3.json"

# Load report
parser = ReportParser(file_path)
report = parser.load()

print("Loaded Report:")
print(report)

issue_manager = IssueManager()

# -----------------------------
# Schema validation
# -----------------------------

schema_issues = SchemaValidator(report).validate()
issue_manager.add_issues(schema_issues)

# -----------------------------
# Calculation validation
# -----------------------------

calc_issues = CalculationValidator(report).validate()
issue_manager.add_issues(calc_issues)

# -----------------------------
# Range validation
# -----------------------------

range_issues = RangeValidator(report).validate()
issue_manager.add_issues(range_issues)

# -----------------------------
# Historical comparison
# -----------------------------

loader = HistoricalLoader(report)
previous_reports = loader.load_previous_reports()

print("\nPrevious Reports:")

if previous_reports:
    for i, prev in enumerate(previous_reports, start=1):
        print(f"\nReport {i}:")
        print(prev)
else:
    print("No previous reports found")

# -----------------------------
# Anomaly detection
# -----------------------------

anomaly_issues = AnomalyDetector(report, previous_reports).detect()
issue_manager.add_issues(anomaly_issues)

print("\nAll Detected Issues:")

all_issues = issue_manager.get_all_issues()

if not all_issues:
    print("No issues detected.")
else:
    for issue in all_issues:
        print(issue)

# -----------------------------
# Issue summary
# -----------------------------

print("\nIssue Severity Summary:")
print(issue_manager.count_by_severity())

# -----------------------------
# Quality scoring
# -----------------------------

scorer = QualityScorer(all_issues)

quality_score = scorer.calculate_score()
status = scorer.get_status(quality_score)

print("\nQuality Evaluation:")
print("Quality Score:", quality_score)
print("Status:", status)

# -----------------------------
# Generate QA report
# -----------------------------

severity_summary = issue_manager.count_by_severity()

report_generator = QAReportGenerator(
    report,
    all_issues,
    severity_summary,
    quality_score,
    status
)

report_generator.generate()

# -----------------------------
# Store report in database
# -----------------------------

db = ReportDatabase()

inserted = db.insert_report(report)

if inserted:
    print("\nReport inserted into database.")
else:
    print("\nReport already exists in database.")