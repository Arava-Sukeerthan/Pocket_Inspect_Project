"""
Analyzer for PocketInspect literature matrix, summary statistics, and research gap identification.
"""
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.literature.schema import (
    PAPERS_SCHEMA_HEADERS,
    BOOLEAN_FIELDS,
    parse_boolean_field
)


class LiteratureAnalyzer:
    """
    Analyzes literature dataset, generates summary statistics, creates literature matrices,
    and produces evidence-backed gap matrices and candidate reports.
    """

    def __init__(self, records: List[Dict[str, str]]):
        self.records = records

    @classmethod
    def from_csv(cls, csv_path: str | Path) -> "LiteratureAnalyzer":
        """Factory method to load records from a CSV file."""
        path = Path(csv_path)
        records = []
        if path.exists():
            with open(path, mode="r", encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    records.append(row)
        return cls(records)

    def filter_papers(
        self,
        boolean_criteria: Optional[Dict[str, bool]] = None,
        domain: Optional[str] = None,
        year_range: Optional[tuple[int, int]] = None,
        keyword: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Filters literature records based on explicit criteria.
        """
        filtered = []
        for r in self.records:
            match = True

            if boolean_criteria:
                for k, expected_val in boolean_criteria.items():
                    val = parse_boolean_field(r.get(k, ""))
                    if val != expected_val:
                        match = False
                        break

            if match and domain:
                r_domain = r.get("domain", "").lower()
                if domain.lower() not in r_domain:
                    match = False

            if match and year_range:
                try:
                    yr = int(r.get("year", "0"))
                    if yr < year_range[0] or yr > year_range[1]:
                        match = False
                except ValueError:
                    match = False

            if match and keyword:
                kw = keyword.lower()
                blob = " ".join(r.values()).lower()
                if kw not in blob:
                    match = False

            if match:
                filtered.append(r)

        return filtered

    def generate_summary_stats(self) -> Dict[str, Any]:
        """
        Generates summary statistics over the literature corpus,
        explicitly tracking known vs unknown/missing data for each characteristic.
        """
        total = len(self.records)
        boolean_stats: Dict[str, Dict[str, Any]] = {}

        for field in BOOLEAN_FIELDS:
            true_count = 0
            false_count = 0
            unknown_count = 0

            for r in self.records:
                val = parse_boolean_field(r.get(field, ""))
                if val is True:
                    true_count += 1
                elif val is False:
                    false_count += 1
                else:
                    unknown_count += 1

            boolean_stats[field] = {
                "true_count": true_count,
                "false_count": false_count,
                "unknown_count": unknown_count,
                "true_percentage": round((true_count / total * 100), 2) if total > 0 else 0.0,
                "known_percentage": round(((true_count + false_count) / total * 100), 2) if total > 0 else 0.0
            }

        # Year distribution
        year_dist: Dict[str, int] = {}
        for r in self.records:
            yr = r.get("year", "").strip() or "Unknown"
            year_dist[yr] = year_dist.get(yr, 0) + 1

        # Domain distribution
        domain_dist: Dict[str, int] = {}
        for r in self.records:
            d = r.get("domain", "").strip() or "Unknown/Unspecified"
            domain_dist[d] = domain_dist.get(d, 0) + 1

        return {
            "total_papers": total,
            "boolean_characteristics": boolean_stats,
            "year_distribution": year_dist,
            "domain_distribution": domain_dist
        }

    def generate_literature_matrix_rows(self) -> List[Dict[str, str]]:
        """
        Generates literature matrix rows summarizing key dimensions per paper.
        """
        matrix_rows = []
        for r in self.records:
            row = {
                "paper_id": r.get("paper_id", ""),
                "title": r.get("title", ""),
                "year": r.get("year", ""),
                "venue": r.get("venue", ""),
                "domain": r.get("domain", "") or "Unspecified",
                "application": r.get("application", "") or "Unspecified",
                "dataset": r.get("dataset", "") or "Unspecified",
                "model": r.get("model", "") or "Unspecified",
                "hardware": r.get("hardware", "") or "Unspecified",
                "smartphone": self._format_bool(r.get("smartphone")),
                "edge_device": self._format_bool(r.get("edge_device")),
                "on_device": self._format_bool(r.get("on_device")),
                "cloud": self._format_bool(r.get("cloud")),
                "adaptive_inference": self._format_bool(r.get("adaptive_inference")),
                "resource_awareness": self._format_bool(r.get("resource_awareness")),
                "energy_evaluation": self._format_bool(r.get("energy_evaluation")),
                "thermal_evaluation": self._format_bool(r.get("thermal_evaluation")),
                "multi_view": self._format_bool(r.get("multi_view")),
                "uncertainty": self._format_bool(r.get("uncertainty")),
                "anomaly_detection": self._format_bool(r.get("anomaly_detection")),
                "latency_evaluation": self._format_bool(r.get("latency_evaluation")),
                "accuracy_metrics": r.get("accuracy_metrics", "") or "Unspecified",
                "limitations": r.get("limitations", "") or "Unspecified",
                "evidence": r.get("evidence", "") or "Unspecified",
                "notes": r.get("notes", "") or ""
            }
            matrix_rows.append(row)
        return matrix_rows

    def write_literature_matrix_csv(self, output_path: str | Path) -> str:
        """
        Writes the generated literature matrix to CSV file.
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        rows = self.generate_literature_matrix_rows()

        fieldnames = [
            "paper_id", "title", "year", "venue", "domain", "application",
            "dataset", "model", "hardware", "smartphone", "edge_device",
            "on_device", "cloud", "adaptive_inference", "resource_awareness",
            "energy_evaluation", "thermal_evaluation", "multi_view", "uncertainty",
            "anomaly_detection", "latency_evaluation", "accuracy_metrics",
            "limitations", "evidence", "notes"
        ]

        with open(path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            if rows:
                writer.writerows(rows)

        return str(path)

    def generate_gap_matrix_rows(self) -> List[Dict[str, str]]:
        """
        Evaluates explicit research dimension combinations against verified papers.
        Generates gap matrix rows with empirical literature support counts.
        """
        # Defined research dimension combinations of interest for PocketInspect
        dimension_combinations = [
            {
                "gap_id": "GAP-001",
                "dimension_name": "Smartphone + Adaptive Inference + Thermal Awareness",
                "description": "Repurposed smartphone edge device with dynamic resource adaptation and thermal-aware execution.",
                "check": lambda r: (
                    parse_boolean_field(r.get("smartphone")) is True and
                    parse_boolean_field(r.get("adaptive_inference")) is True and
                    parse_boolean_field(r.get("thermal_evaluation")) is True
                )
            },
            {
                "gap_id": "GAP-002",
                "dimension_name": "3D-Print Defect Inspection + Resource-Aware Edge AI",
                "description": "Visual inspection of 3D prints or small manufactured parts using resource-aware edge inference.",
                "check": lambda r: (
                    ("3d" in r.get("domain", "").lower() or "print" in r.get("domain", "").lower() or "manufactur" in r.get("domain", "").lower() or "inspection" in r.get("domain", "").lower()) and
                    (parse_boolean_field(r.get("edge_device")) is True or parse_boolean_field(r.get("smartphone")) is True) and
                    parse_boolean_field(r.get("resource_awareness")) is True
                )
            },
            {
                "gap_id": "GAP-003",
                "dimension_name": "Smartphone + On-Device Inference + Uncertainty Estimation",
                "description": "On-device smartphone visual inspection with prediction uncertainty quantification and OOD detection.",
                "check": lambda r: (
                    parse_boolean_field(r.get("smartphone")) is True and
                    parse_boolean_field(r.get("on_device")) is True and
                    parse_boolean_field(r.get("uncertainty")) is True
                )
            },
            {
                "gap_id": "GAP-004",
                "dimension_name": "Smartphone + Multi-View Inspection + On-Device Execution",
                "description": "Multi-view image acquisition and on-device visual defect aggregation on mobile smartphones.",
                "check": lambda r: (
                    parse_boolean_field(r.get("smartphone")) is True and
                    parse_boolean_field(r.get("multi_view")) is True and
                    parse_boolean_field(r.get("on_device")) is True
                )
            },
            {
                "gap_id": "GAP-005",
                "dimension_name": "Adaptive Inference + Thermal & Energy Evaluation",
                "description": "Adaptive compute algorithms evaluated simultaneously for thermal throttling and battery energy drain.",
                "check": lambda r: (
                    parse_boolean_field(r.get("adaptive_inference")) is True and
                    parse_boolean_field(r.get("thermal_evaluation")) is True and
                    parse_boolean_field(r.get("energy_evaluation")) is True
                )
            },
            {
                "gap_id": "GAP-006",
                "dimension_name": "3D-Print Defect Inspection + Anomaly Detection + On-Device Execution",
                "description": "Unsupervised or semi-supervised anomaly detection for 3D prints running on-device.",
                "check": lambda r: (
                    ("3d" in r.get("domain", "").lower() or "print" in r.get("domain", "").lower() or "manufactur" in r.get("domain", "").lower()) and
                    parse_boolean_field(r.get("anomaly_detection")) is True and
                    parse_boolean_field(r.get("on_device")) is True
                )
            }
        ]

        gap_rows = []
        for combo in dimension_combinations:
            matching_papers = []
            for r in self.records:
                if combo["check"](r):
                    pid = r.get("paper_id", "").strip()
                    if pid:
                        matching_papers.append(pid)

            support_count = len(matching_papers)
            supporting_ids_str = ", ".join(matching_papers) if matching_papers else "None"

            # Strict research rule: Never label automatically as "novel".
            # Tag as candidate for researcher review.
            if support_count == 0:
                gap_status = "Unexplored in Current Corpus (Candidate Gap - Requires Researcher Verification)"
            elif support_count <= 2:
                gap_status = "Sparsely Covered (Candidate Gap - Requires Researcher Verification)"
            else:
                gap_status = "Covered in Literature"

            gap_rows.append({
                "gap_id": combo["gap_id"],
                "dimension_combination": combo["dimension_name"],
                "description": combo["description"],
                "literature_support_count": str(support_count),
                "supporting_paper_ids": supporting_ids_str,
                "gap_status": gap_status,
                "verification_status": "Pending Researcher Review"
            })

        return gap_rows

    def write_gap_matrix_csv(self, output_path: str | Path) -> str:
        """
        Writes gap analysis matrix to CSV file.
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        rows = self.generate_gap_matrix_rows()

        fieldnames = [
            "gap_id",
            "dimension_combination",
            "description",
            "literature_support_count",
            "supporting_paper_ids",
            "gap_status",
            "verification_status"
        ]

        with open(path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            if rows:
                writer.writerows(rows)

        return str(path)

    def generate_gap_candidates_markdown(self) -> str:
        """
        Generates markdown candidate report for researcher review.
        """
        gap_rows = self.generate_gap_matrix_rows()
        stats = self.generate_summary_stats()

        md = []
        md.append("# PocketInspect: Research Gap Candidates & Literature Analysis Report")
        md.append("")
        md.append("> **Important Research Notice**: Research gaps reported here represent empirical coverage analysis across verified literature records in `research/literature/papers.csv`. Candidates require explicit researcher verification before claiming scientific contribution.")
        md.append("")
        md.append("## 1. Literature Corpus Overview")
        md.append("")
        md.append(f"- **Total Verified Papers**: {stats['total_papers']}")
        md.append("")

        if stats['total_papers'] == 0:
            md.append("> *Note: `papers.csv` currently contains 0 paper entries. As verified papers are ingested, this matrix will update automatically.*")
            md.append("")
        else:
            md.append("| Characteristic | True Count | False Count | Unknown Count | % True | % Known |")
            md.append("| :--- | :---: | :---: | :---: | :---: | :---: |")
            for char, cdata in stats['boolean_characteristics'].items():
                md.append(f"| `{char}` | {cdata['true_count']} | {cdata['false_count']} | {cdata['unknown_count']} | {cdata['true_percentage']}% | {cdata['known_percentage']}% |")
            md.append("")

        md.append("## 2. Research Dimension Gap Matrix")
        md.append("")
        md.append("| Gap ID | Dimension Combination | Support Count | Supporting Papers | Gap Status | Researcher Action |")
        md.append("| :--- | :--- | :---: | :--- | :--- | :--- |")

        for row in gap_rows:
            md.append(f"| **{row['gap_id']}** | {row['dimension_combination']} | {row['literature_support_count']} | `{row['supporting_paper_ids']}` | {row['gap_status']} | `{row['verification_status']}` |")

        md.append("")
        md.append("## 3. Detailed Gap Descriptions & Researcher Verification Directives")
        md.append("")

        for row in gap_rows:
            md.append(f"### {row['gap_id']}: {row['dimension_combination']}")
            md.append(f"- **Description**: {row['description']}")
            md.append(f"- **Literature Support Count**: {row['literature_support_count']}")
            md.append(f"- **Supporting Paper IDs**: `{row['supporting_paper_ids']}`")
            md.append(f"- **Current Status**: {row['gap_status']}")
            md.append(f"- **Verification Protocol**:")
            md.append(f"  1. Verify if relevant literature in `research/literature/papers.csv` is missing papers in this domain.")
            md.append(f"  2. Review `evidence` and `limitations` columns of matching papers if support count > 0.")
            md.append(f"  3. Explicitly confirm or reject candidate gap status before freezing research contribution.")
            md.append("")

        return "\n".join(md)

    def write_gap_candidates_markdown(self, output_path: str | Path) -> str:
        """Writes candidate report markdown file."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        content = self.generate_gap_candidates_markdown()
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(content)
        return str(path)

    @staticmethod
    def _format_bool(val: Any) -> str:
        """Formats boolean value into clean string without inferring missing data."""
        parsed = parse_boolean_field(val)
        if parsed is True:
            return "true"
        if parsed is False:
            return "false"
        return "unknown"
