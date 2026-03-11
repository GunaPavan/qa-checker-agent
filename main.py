import streamlit as st
import tempfile
import json

from core.parser import ReportParser
from core.schema_validator import SchemaValidator
from core.calculation_validator import CalculationValidator
from core.range_validator import RangeValidator
from core.historical_loader import HistoricalLoader
from core.anomaly_detector import AnomalyDetector
from core.issue_manager import IssueManager
from core.quality_scorer import QualityScorer
from core.database import ReportDatabase


st.set_page_config(page_title="QA Compliance Checker", layout="wide")

st.title("QA Compliance Checker Agent")
st.write("Upload a compliance report to validate its quality and detect issues.")

uploaded_file = st.file_uploader("Upload Report", type=["json", "csv"])


if uploaded_file:

    # Preserve file extension for parser
    suffix = uploaded_file.name.split(".")[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        tmp.write(uploaded_file.read())
        file_path = tmp.name

    # Parse report
    parser = ReportParser(file_path)
    report = parser.load()

    st.subheader("Loaded Report")
    st.json(report)

    issue_manager = IssueManager()

    # -----------------------------
    # Schema Validation
    # -----------------------------

    with st.expander("Schema Validation", expanded=True):

        schema_issues = SchemaValidator(report).validate()
        issue_manager.add_issues(schema_issues)

        if not schema_issues:
            st.success("Schema validation passed")
        else:
            for issue in schema_issues:
                st.warning(issue)

    # -----------------------------
    # Calculation Validation
    # -----------------------------

    with st.expander("Calculation Validation"):

        calc_issues = CalculationValidator(report).validate()
        issue_manager.add_issues(calc_issues)

        if not calc_issues:
            st.success("Calculation validation passed")
        else:
            for issue in calc_issues:
                st.warning(issue)

    # -----------------------------
    # Range Validation
    # -----------------------------

    with st.expander("Range Validation"):

        range_issues = RangeValidator(report).validate()
        issue_manager.add_issues(range_issues)

        if not range_issues:
            st.success("Range validation passed")
        else:
            for issue in range_issues:
                st.warning(issue)

    # -----------------------------
    # Historical Comparison
    # -----------------------------

    with st.expander("Historical Comparison"):

        loader = HistoricalLoader(report)
        previous_reports = loader.load_previous_reports()

        if previous_reports:
            st.subheader("Previous Reports")

            for i, prev in enumerate(previous_reports, start=1):
                st.markdown(f"**Report {i}**")
                st.json(prev)

        else:
            st.info("No previous reports found.")

    # -----------------------------
    # Anomaly Detection
    # -----------------------------

    with st.expander("Anomaly Detection"):

        anomaly_issues = AnomalyDetector(report, previous_reports).detect()
        issue_manager.add_issues(anomaly_issues)

        if not anomaly_issues:
            st.success("No anomalies detected")
        else:
            for issue in anomaly_issues:
                st.error(issue)

    # -----------------------------
    # Aggregated Issues
    # -----------------------------

    all_issues = issue_manager.get_all_issues()

    st.subheader("All Detected Issues")

    if not all_issues:
        st.success("No issues detected.")
    else:
        for issue in all_issues:
            st.error(
                f"{issue['issue_type']} | Field: {issue['field']} | Severity: {issue['severity']} | {issue['description']}"
            )

    # -----------------------------
    # Issue Summary
    # -----------------------------

    severity_summary = issue_manager.count_by_severity()

    st.subheader("Issue Severity Summary")
    st.write(severity_summary)

    # -----------------------------
    # Quality Scoring
    # -----------------------------

    scorer = QualityScorer(all_issues)

    quality_score = scorer.calculate_score()
    status = scorer.get_status(quality_score)

    st.subheader("Quality Evaluation")

    col1, col2 = st.columns(2)

    col1.metric("Quality Score", quality_score)
    col2.metric("Status", status)

    # -----------------------------
    # Downloadable QA Report
    # -----------------------------

    report_output = {
        "report_id": report.get("report_id"),
        "entity": report.get("entity"),
        "report_type": report.get("report_type"),
        "date": report.get("report_date"),
        "issues": all_issues,
        "severity_summary": severity_summary,
        "quality_score": quality_score,
        "status": status
    }

    report_json = json.dumps(report_output, indent=4)

    st.download_button(
        label="Download QA Report",
        data=report_json,
        file_name="qa_validation_report.json",
        mime="application/json"
    )

    # -----------------------------
    # SAVE REPORT (Prevent Duplicate)
    # -----------------------------

    db = ReportDatabase()

    inserted = db.insert_report(report)

    if inserted:
        st.success("Report stored in database.")
    else:
        st.warning("This report already exists in the database.")