"""
CLI Utility for PocketInspect literature management, validation, matrix generation, and gap analysis.
"""
import argparse
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.literature import LiteratureValidator, LiteratureAnalyzer, MatrixExporter


def cmd_validate(args):
    papers_path = Path(args.papers)
    print(f"[Literature Manager] Validating: {papers_path}")
    validator = LiteratureValidator()
    report = validator.validate_file(papers_path)

    print(f"Total Records: {report['total_records']}")
    if report["is_valid"]:
        print("Status: VALID (Schema checks passed)")
    else:
        print("Status: INVALID (Schema errors found)")
        for err in report["schema_errors"]:
            print(f"  - ERROR: {err}")

    if report["warnings"]:
        print(f"Warnings ({len(report['warnings'])}):")
        for w in report["warnings"]:
            print(f"  - WARN: {w}")

    if report["duplicates"]:
        print(f"Duplicates Detected ({len(report['duplicates'])}):")
        for d in report["duplicates"]:
            print(f"  - DUP [{d['type']}]: Row {d['row_1']} ({d['paper_id_1']}) vs Row {d['row_2']} ({d['paper_id_2']})")

    return 0 if report["is_valid"] else 1


def cmd_stats(args):
    papers_path = Path(args.papers)
    analyzer = LiteratureAnalyzer.from_csv(papers_path)
    stats = analyzer.generate_summary_stats()

    print("==================================================")
    print(f"Literature Summary Statistics ({papers_path})")
    print("==================================================")
    print(f"Total Verified Papers: {stats['total_papers']}")
    print("")

    if stats["total_papers"] > 0:
        print(f"{'Characteristic':<22} | {'True':<6} | {'False':<6} | {'Unknown':<8} | {'% True':<8}")
        print("-" * 62)
        for char, cdata in stats["boolean_characteristics"].items():
            print(f"{char:<22} | {cdata['true_count']:<6} | {cdata['false_count']:<6} | {cdata['unknown_count']:<8} | {cdata['true_percentage']:<8}%")
    else:
        print("Notice: No papers currently in papers.csv.")
    return 0


def cmd_matrix(args):
    papers_path = Path(args.papers)
    out_path = Path(args.out) if args.out else PROJECT_ROOT / "research" / "literature" / "literature_matrix.csv"

    analyzer = LiteratureAnalyzer.from_csv(papers_path)
    written_file = analyzer.write_literature_matrix_csv(out_path)
    print(f"[Literature Manager] Literature matrix generated at: {written_file}")
    return 0


def cmd_gap(args):
    papers_path = Path(args.papers)
    out_csv = Path(args.out_csv) if args.out_csv else PROJECT_ROOT / "research" / "gap_analysis" / "gap_matrix.csv"
    out_md = Path(args.out_md) if args.out_md else PROJECT_ROOT / "research" / "gap_analysis" / "gap_candidates.md"

    analyzer = LiteratureAnalyzer.from_csv(papers_path)
    written_csv = analyzer.write_gap_matrix_csv(out_csv)
    written_md = analyzer.write_gap_candidates_markdown(out_md)

    print(f"[Literature Manager] Gap matrix CSV generated at: {written_csv}")
    print(f"[Literature Manager] Gap candidates report generated at: {written_md}")
    return 0


def cmd_export(args):
    papers_path = Path(args.papers)
    analyzer = LiteratureAnalyzer.from_csv(papers_path)
    rows = analyzer.generate_literature_matrix_rows()

    if args.format == "latex":
        out_str = MatrixExporter.export_literature_latex(rows)
    else:
        out_str = MatrixExporter.export_literature_markdown(rows)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out_str)
        print(f"[Literature Manager] Exported literature matrix ({args.format}) to: {args.out}")
    else:
        print(out_str)
    return 0


def cmd_all(args):
    print("--- 1. Validation ---")
    cmd_validate(args)
    print("\n--- 2. Summary Statistics ---")
    cmd_stats(args)
    print("\n--- 3. Generating Literature Matrix ---")
    cmd_matrix(args)
    print("\n--- 4. Generating Gap Matrix & Candidate Report ---")
    cmd_gap(args)
    print("\nFull literature pipeline execution complete.")
    return 0


def main():
    default_papers = PROJECT_ROOT / "research" / "literature" / "papers.csv"

    parser = argparse.ArgumentParser(description="PocketInspect Literature Management Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Validate
    p_val = subparsers.add_parser("validate", help="Validate papers.csv schema and duplicate entries")
    p_val.add_argument("--papers", default=str(default_papers), help="Path to papers.csv")

    # Stats
    p_stat = subparsers.add_parser("stats", help="Print summary statistics of verified literature")
    p_stat.add_argument("--papers", default=str(default_papers), help="Path to papers.csv")

    # Matrix
    p_mat = subparsers.add_parser("matrix", help="Generate literature_matrix.csv")
    p_mat.add_argument("--papers", default=str(default_papers), help="Path to papers.csv")
    p_mat.add_argument("--out", default=None, help="Output matrix CSV path")

    # Gap
    p_gap = subparsers.add_parser("gap", help="Generate gap_matrix.csv and gap_candidates.md")
    p_gap.add_argument("--papers", default=str(default_papers), help="Path to papers.csv")
    p_gap.add_argument("--out-csv", default=None, help="Output gap matrix CSV path")
    p_gap.add_argument("--out-md", default=None, help="Output gap candidates Markdown path")

    # Export
    p_exp = subparsers.add_parser("export", help="Export literature matrix to Markdown or LaTeX format")
    p_exp.add_argument("--papers", default=str(default_papers), help="Path to papers.csv")
    p_exp.add_argument("--format", choices=["markdown", "latex"], default="markdown", help="Export format")
    p_exp.add_argument("--out", default=None, help="Output file path (optional)")

    # All
    p_all = subparsers.add_parser("all", help="Run full literature pipeline")
    p_all.add_argument("--papers", default=str(default_papers), help="Path to papers.csv")
    p_all.add_argument("--out", default=None, help="Output path")
    p_all.add_argument("--out-csv", default=None, help="Output gap CSV path")
    p_all.add_argument("--out-md", default=None, help="Output gap MD path")

    args = parser.parse_args()

    if args.command == "validate":
        sys.exit(cmd_validate(args))
    elif args.command == "stats":
        sys.exit(cmd_stats(args))
    elif args.command == "matrix":
        sys.exit(cmd_matrix(args))
    elif args.command == "gap":
        sys.exit(cmd_gap(args))
    elif args.command == "export":
        sys.exit(cmd_export(args))
    elif args.command == "all":
        sys.exit(cmd_all(args))


if __name__ == "__main__":
    main()
