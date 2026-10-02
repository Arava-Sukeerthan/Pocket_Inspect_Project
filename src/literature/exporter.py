"""
Exporter utilities for converting literature and gap matrices to Markdown and LaTeX tabular formats.
"""
from typing import List, Dict, Any


class MatrixExporter:
    """
    Exports literature and gap matrices to Markdown tables and LaTeX tabular code blocks.
    """

    @staticmethod
    def export_literature_markdown(rows: List[Dict[str, str]]) -> str:
        """
        Formats literature matrix rows as Markdown table.
        """
        if not rows:
            return "_No literature papers currently present in corpus._\n"

        headers = [
            "Paper ID", "Title", "Year", "Venue", "Domain", "Hardware",
            "Smartphone", "On-Device", "Adaptive", "Resource-Aware", "Thermal Eval",
            "Confidence Gating"
        ]
        
        md = []
        md.append("| " + " | ".join(headers) + " |")
        md.append("| " + " | ".join([":---"] * len(headers)) + " |")

        for r in rows:
            line = [
                r.get("paper_id", ""),
                r.get("title", ""),
                r.get("year", ""),
                r.get("venue", ""),
                r.get("domain", ""),
                r.get("hardware", ""),
                r.get("smartphone", ""),
                r.get("on_device", ""),
                r.get("adaptive_inference", ""),
                r.get("resource_awareness", ""),
                r.get("thermal_evaluation", ""),
                r.get("confidence_gating", "")
            ]
            # Escape pipe symbols in strings
            line_clean = [str(x).replace("|", "\\|") for x in line]
            md.append("| " + " | ".join(line_clean) + " |")

        return "\n".join(md) + "\n"

    @staticmethod
    def export_literature_latex(rows: List[Dict[str, str]]) -> str:
        """
        Formats literature matrix rows as LaTeX tabular environment.
        """
        if not rows:
            return "% No literature papers in corpus.\n"

        tex = []
        tex.append("\\begin{table*}[t]")
        tex.append("\\centering")
        tex.append("\\caption{Summary of Verified Literature for PocketInspect}")
        tex.append("\\label{tab:literature_matrix}")
        tex.append("\\begin{tabular}{lllccccc}")
        tex.append("\\toprule")
        tex.append("ID & Title & Year & Hardware & Smartphone & On-Device & Adaptive & Thermal \\\\")
        tex.append("\\midrule")

        for r in rows:
            title_short = r.get("title", "")
            if len(title_short) > 35:
                title_short = title_short[:32] + "..."
            
            line = [
                r.get("paper_id", ""),
                title_short,
                r.get("year", ""),
                r.get("hardware", ""),
                "\\checkmark" if r.get("smartphone") == "true" else ("\\times" if r.get("smartphone") == "false" else "-"),
                "\\checkmark" if r.get("on_device") == "true" else ("\\times" if r.get("on_device") == "false" else "-"),
                "\\checkmark" if r.get("adaptive_inference") == "true" else ("\\times" if r.get("adaptive_inference") == "false" else "-"),
                "\\checkmark" if r.get("thermal_evaluation") == "true" else ("\\times" if r.get("thermal_evaluation") == "false" else "-")
            ]
            clean_line = [str(x).replace("&", "\\&").replace("_", "\\_") for x in line]
            tex.append(" & ".join(clean_line) + " \\\\")

        tex.append("\\bottomrule")
        tex.append("\\end{tabular}")
        tex.append("\\end{table*}")
        return "\n".join(tex) + "\n"

    @staticmethod
    def export_gap_latex(rows: List[Dict[str, str]]) -> str:
        """
        Formats gap matrix rows as LaTeX tabular environment.
        """
        if not rows:
            return "% No gap matrix entries.\n"

        tex = []
        tex.append("\\begin{table}[t]")
        tex.append("\\centering")
        tex.append("\\caption{Research Gap Analysis Matrix}")
        tex.append("\\label{tab:gap_matrix}")
        tex.append("\\begin{tabular}{llcl}")
        tex.append("\\toprule")
        tex.append("Gap ID & Dimension Combination & Support Count & Status \\\\")
        tex.append("\\midrule")

        for r in rows:
            line = [
                r.get("gap_id", ""),
                r.get("dimension_combination", ""),
                r.get("literature_support_count", "0"),
                r.get("gap_status", "")
            ]
            clean_line = [str(x).replace("&", "\\&").replace("_", "\\_") for x in line]
            tex.append(" & ".join(clean_line) + " \\\\")

        tex.append("\\bottomrule")
        tex.append("\\end{tabular}")
        tex.append("\\end{table}")
        return "\n".join(tex) + "\n"
