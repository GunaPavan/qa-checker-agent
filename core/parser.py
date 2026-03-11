import json
import pandas as pd
from pathlib import Path


class ReportParser:
    """
    Responsible for loading compliance reports
    from supported formats and converting them
    into a standard Python dictionary structure.
    """

    SUPPORTED_FORMATS = [".json", ".csv"]

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load(self):
        """Load the report depending on file type."""

        if not self.file_path.exists():
            raise FileNotFoundError(f"Report file not found: {self.file_path}")

        suffix = self.file_path.suffix.lower()

        if suffix == ".json":
            return self._load_json()

        elif suffix == ".csv":
            return self._load_csv()

        else:
            raise ValueError(f"Unsupported report format: {suffix}")

    def _load_json(self):
        """Load JSON report."""

        with open(self.file_path, "r") as f:
            data = json.load(f)

        return data

    def _load_csv(self):
        """
        Convert CSV report to dictionary format.
        Expected format: key,value
        """

        df = pd.read_csv(self.file_path)

        report_dict = dict(zip(df["key"], df["value"]))

        return report_dict
