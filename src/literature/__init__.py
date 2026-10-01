"""
PocketInspect Literature & Research Gap Management Subsystem.
"""

from src.literature.schema import (
    PAPERS_SCHEMA_HEADERS,
    BOOLEAN_FIELDS,
    REQUIRED_FIELDS,
    parse_boolean_field,
    normalize_title,
    normalize_doi
)
from src.literature.validator import LiteratureValidator
from src.literature.analyzer import LiteratureAnalyzer
from src.literature.exporter import MatrixExporter

__all__ = [
    "PAPERS_SCHEMA_HEADERS",
    "BOOLEAN_FIELDS",
    "REQUIRED_FIELDS",
    "parse_boolean_field",
    "normalize_title",
    "normalize_doi",
    "LiteratureValidator",
    "LiteratureAnalyzer",
    "MatrixExporter"
]
