"""
Validator for PocketInspect literature papers.csv repository files.
"""
import csv
from pathlib import Path
from typing import List, Dict, Any, Tuple
from src.literature.schema import (
    PAPERS_SCHEMA_HEADERS,
    BOOLEAN_FIELDS,
    REQUIRED_FIELDS,
    parse_boolean_field,
    normalize_title,
    normalize_doi,
    TRUTHY_VALUES,
    FALSY_VALUES,
    UNKNOWN_VALUES
)


class LiteratureValidator:
    """
    Validates papers.csv structure, headers, data types, required fields, and duplicate papers.
    """

    def __init__(self, headers: List[str] = PAPERS_SCHEMA_HEADERS):
        self.expected_headers = headers

    def validate_file(self, file_path: str | Path) -> Dict[str, Any]:
        """
        Reads and validates a papers.csv file.
        Returns a detailed validation report dictionary.
        """
        path = Path(file_path)
        if not path.exists():
            return {
                "is_valid": False,
                "file_path": str(path),
                "total_records": 0,
                "schema_errors": [f"File does not exist: {path}"],
                "warnings": [],
                "duplicates": []
            }

        with open(path, mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            try:
                headers = next(reader)
            except StopIteration:
                return {
                    "is_valid": False,
                    "file_path": str(path),
                    "total_records": 0,
                    "schema_errors": ["File is completely empty"],
                    "warnings": [],
                    "duplicates": []
                }

        # Check headers
        header_errors = self._validate_headers(headers)
        if header_errors:
            return {
                "is_valid": False,
                "file_path": str(path),
                "total_records": 0,
                "schema_errors": header_errors,
                "warnings": [],
                "duplicates": []
            }

        # Read records with DictReader
        records: List[Dict[str, str]] = []
        with open(path, mode="r", encoding="utf-8-sig", newline="") as f:
            dict_reader = csv.DictReader(f)
            for row in dict_reader:
                records.append(row)

        return self.validate_records(records, str(path))

    def _validate_headers(self, headers: List[str]) -> List[str]:
        """Validates CSV headers against expected schema."""
        errors = []
        clean_headers = [h.strip() for h in headers]
        if clean_headers != self.expected_headers:
            missing = set(self.expected_headers) - set(clean_headers)
            extra = set(clean_headers) - set(self.expected_headers)
            if missing:
                errors.append(f"Missing required schema columns: {sorted(list(missing))}")
            if extra:
                errors.append(f"Unexpected extra columns: {sorted(list(extra))}")
            if not missing and not extra and clean_headers != self.expected_headers:
                errors.append(f"Column order mismatch. Expected: {self.expected_headers}, got: {clean_headers}")
        return errors

    def validate_records(self, records: List[Dict[str, str]], source_name: str = "in-memory") -> Dict[str, Any]:
        """
        Validates a list of paper record dicts.
        """
        schema_errors: List[str] = []
        warnings: List[str] = []
        duplicates: List[Dict[str, Any]] = []

        seen_dois: Dict[str, Tuple[int, str]] = {}     # norm_doi -> (row_idx, paper_id)
        seen_titles: Dict[str, Tuple[int, str]] = {}   # norm_title -> (row_idx, paper_id)
        seen_ids: Dict[str, int] = {}                  # paper_id -> row_idx

        for idx, record in enumerate(records, start=1):
            paper_id = record.get("paper_id", "").strip()
            title = record.get("title", "").strip()
            year_str = record.get("year", "").strip()
            doi = record.get("doi", "").strip()

            # Required field checks
            for field in REQUIRED_FIELDS:
                val = record.get(field, "").strip()
                if not val:
                    warnings.append(f"Row {idx} (paper_id='{paper_id}'): missing value for required field '{field}'")

            # Unique paper_id check
            if paper_id:
                if paper_id in seen_ids:
                    schema_errors.append(f"Row {idx}: duplicate paper_id '{paper_id}' (first seen at row {seen_ids[paper_id]})")
                else:
                    seen_ids[paper_id] = idx

            # Year data type check
            if year_str and not year_str.lower() in UNKNOWN_VALUES:
                try:
                    year_val = int(year_str)
                    if year_val < 1900 or year_val > 2030:
                        warnings.append(f"Row {idx} ('{paper_id}'): year value {year_val} is out of expected range (1900-2030)")
                except ValueError:
                    schema_errors.append(f"Row {idx} ('{paper_id}'): invalid year value '{year_str}' (expected integer)")

            # Boolean field validation
            for b_field in BOOLEAN_FIELDS:
                val = record.get(b_field, "").strip()
                if val:
                    lval = val.lower()
                    if lval not in TRUTHY_VALUES and lval not in FALSY_VALUES and lval not in UNKNOWN_VALUES:
                        warnings.append(f"Row {idx} ('{paper_id}'): unstandardized boolean value '{val}' in field '{b_field}'. Use 'true' or 'false'.")

            # DOI Duplicate detection
            if doi:
                norm_doi = normalize_doi(doi)
                if norm_doi:
                    if norm_doi in seen_dois:
                        prev_idx, prev_id = seen_dois[norm_doi]
                        duplicates.append({
                            "type": "DOI match",
                            "doi": doi,
                            "paper_id_1": prev_id,
                            "row_1": prev_idx,
                            "paper_id_2": paper_id,
                            "row_2": idx
                        })
                    else:
                        seen_dois[norm_doi] = (idx, paper_id)

            # Title Duplicate detection
            if title:
                norm_title = normalize_title(title)
                if norm_title:
                    if norm_title in seen_titles:
                        prev_idx, prev_id = seen_titles[norm_title]
                        duplicates.append({
                            "type": "Title match",
                            "title": title,
                            "paper_id_1": prev_id,
                            "row_1": prev_idx,
                            "paper_id_2": paper_id,
                            "row_2": idx
                        })
                    else:
                        seen_titles[norm_title] = (idx, paper_id)

        is_valid = len(schema_errors) == 0

        return {
            "is_valid": is_valid,
            "source": source_name,
            "total_records": len(records),
            "schema_errors": schema_errors,
            "warnings": warnings,
            "duplicates": duplicates
        }
