"""
Schema definitions and field metadata for PocketInspect literature management.
"""
from typing import List, Set, Dict

# Exact 29-column schema required for papers.csv
PAPERS_SCHEMA_HEADERS: List[str] = [
    "paper_id",
    "title",
    "authors",
    "year",
    "venue",
    "doi",
    "url",
    "domain",
    "application",
    "dataset",
    "model",
    "hardware",
    "smartphone",
    "edge_device",
    "on_device",
    "cloud",
    "adaptive_inference",
    "resource_awareness",
    "energy_evaluation",
    "thermal_evaluation",
    "multi_view",
    "uncertainty",
    "anomaly_detection",
    "latency_evaluation",
    "accuracy_metrics",
    "limitations",
    "future_work",
    "evidence",
    "notes"
]

# Fields that represent boolean characteristics (true / false / unknown)
BOOLEAN_FIELDS: Set[str] = {
    "smartphone",
    "edge_device",
    "on_device",
    "cloud",
    "adaptive_inference",
    "resource_awareness",
    "energy_evaluation",
    "thermal_evaluation",
    "multi_view",
    "uncertainty",
    "anomaly_detection",
    "latency_evaluation"
}

# Fields required for minimum valid paper entry
REQUIRED_FIELDS: Set[str] = {
    "paper_id",
    "title",
    "authors",
    "year"
}

# Recognized representations for True / False values
TRUTHY_VALUES: Set[str] = {"true", "1", "yes", "y", "t"}
FALSY_VALUES: Set[str] = {"false", "0", "no", "n", "f"}
UNKNOWN_VALUES: Set[str] = {"", "unknown", "unk", "n/a", "none", "null"}

def parse_boolean_field(val: str) -> bool | None:
    """
    Parses a string into True, False, or None (if unknown/unspecified).
    Does not infer values for missing/unknown data.
    """
    if val is None:
        return None
    s = str(val).strip().lower()
    if s in TRUTHY_VALUES:
        return True
    if s in FALSY_VALUES:
        return False
    return None

def normalize_title(title: str) -> str:
    """
    Normalizes a paper title for duplicate detection.
    Converts to lowercase and strips non-alphanumeric characters.
    """
    if not title:
        return ""
    import re
    return re.sub(r'[^a-z0-9]', '', title.lower())

def normalize_doi(doi: str) -> str:
    """
    Normalizes a DOI string for duplicate detection.
    Strips URL prefixes and converts to lowercase.
    """
    if not doi:
        return ""
    d = doi.strip().lower()
    for prefix in ["https://doi.org/", "http://doi.org/", "doi:"]:
        if d.startswith(prefix):
            d = d[len(prefix):]
    return d.strip()
