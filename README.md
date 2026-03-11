# QA Compliance Checker Agent

## Overview
The QA Compliance Checker Agent is an automated validation system designed to verify the quality and accuracy of structured compliance reports.

The system performs multiple validation checks to detect issues such as:
- Missing report fields
- Calculation inconsistencies
- Invalid metric ranges
- Abnormal changes compared to historical reports

After performing these validations, the system generates a QA evaluation report with a quality score indicating the reliability of the uploaded report.

The project includes an interactive web interface built with Streamlit where users can upload reports, analyze them, and download validation results.

## System Architecture
The validation system follows a modular processing pipeline.

Report Upload
↓
Report Parser
↓
Schema Validation
↓
Calculation Validation
↓
Range Validation
↓
Historical Report Retrieval
↓
Anomaly Detection
↓
Issue Aggregation
↓
Quality Score Calculation
↓
QA Validation Report


Each validation stage is implemented as an independent module.

## Project Structure

qa-checker-agent
│
├── core
│ ├── anomaly_detector.py
│ ├── calculation_validator.py
│ ├── database.py
│ ├── historical_loader.py
│ ├── issue_manager.py
│ ├── parser.py
│ ├── quality_scorer.py
│ ├── range_validator.py
│ └── schema_validator.py
│
├── data
│ └── reports
│ ├── report1.json
│ ├── report2.json
│ └── report3.json
│
├── output
│
├── tests
│ └── test_functionality.py
│
├
├── .gitignore
├── LICENSE
├── main.py
├── requirements.txt
├── README.md
└── INSTALL.md


## Validation Logic
The system applies several validation checks to each uploaded report.

### Schema Validation
Ensures required report fields exist:
- report_id
- report_type
- entity
- report_date
- metrics

If fields are missing, a MISSING_DATA issue is generated.

### Calculation Validation
Verifies that totals match the sum of subcategories.

Example rule:
sum(revenue_breakdown) == total_revenue

If totals do not match:
CALCULATION_ERROR

### Range Validation
Ensures numeric metrics fall within valid ranges.

Examples:
0 ≤ compliance_score ≤ 100
revenue ≥ 0
Invalid values trigger:
RANGE_ERROR


### Historical Comparison
Reports are stored in a PostgreSQL database.

When a new report is uploaded, the system retrieves all previous reports for the same entity and report type.

These historical reports provide context for anomaly detection.

### Anomaly Detection
Metric changes are compared against historical reports.

Percentage change formula:
Change (%) = ((Current − Previous) / Previous) × 100


Severity thresholds:

| Change | Severity |
|--------|----------|
| 30% | WARNING |
| 50% | CRITICAL |

Example:
Previous revenue = 100000
Current revenue = 160000
Change = 60%
Severity = CRITICAL


### Quality Scoring
A quality score summarizes report reliability.

The score starts at 100 and deductions are applied depending on issue severity.

Example penalties:

| Severity | Penalty |
|----------|---------|
| CRITICAL | -40 |
| HIGH | -25 |
| MEDIUM | -15 |
| LOW | -5 |

Final status:

| Score | Status |
|-------|--------|
| ≥ 80 | PASS |
| < 80 | FAIL |

## Expected Report Format
To test the system through the interface, reports must follow this structure.

Example report:
```json
{
  "report_id": "REP-019",
  "report_type": "compliance",
  "entity": "Department_A",
  "report_date": "2026-02-01",
  "metrics": {
    "total_revenue": 90000,
    "revenue_breakdown": {
      "product": 30000,
      "services": 30000,
      "subscriptions": 30000
    },
    "compliance_score": 90
  }
}

Field Descriptions
Field	Description
report_id	Unique identifier for the report
report_type	Type of report
entity	Reporting department or organization
report_date	Report date used for historical comparison
metrics	Numeric metrics used for validation

Example testing scenarios:
Valid Report
Upload a correctly structured report.

Expected result:


No issues detected
Quality Score: 100
Status: PASS
Calculation Error
Example modification:


revenue_breakdown total = 100000
reported total_revenue = 105000
Expected result:


CALCULATION_ERROR
Range Error
Example:


compliance_score = 920
Expected result:


RANGE_ERROR
Historical Anomaly
Upload two reports with significant differences.

Example:

Report 1


total_revenue = 90000
Report 2

total_revenue = 160000
Expected result:

ANOMALY_DETECTED
Severity: CRITICAL
Running the Application
Instructions for installing dependencies and running the application locally are provided in: INSTALL.md

Technologies Used
Python

Streamlit

PostgreSQL

Supabase

psycopg2

Summary
The QA Compliance Checker Agent provides an automated framework for validating compliance reports.

By combining rule-based validation, historical comparison, and quality scoring, the system helps detect inconsistencies and ensures that reports maintain high data integrity standards.