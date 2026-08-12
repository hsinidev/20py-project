"""Export functions: JSON-LD and PDF Executive Summary."""
import json
from datetime import datetime
from pathlib import Path


def export_jsonld(results: list, path: str) -> bool:
    """Export all search results as JSON-LD structured data."""
    doc = {
        "@context": "https://schema.org",
        "@type":    "Dataset",
        "name":     "Omni-Engine Visibility & Attribution Report",
        "creator":  {"@type": "Person", "name": "HSINI MOHAMED"},
        "dateCreated": datetime.now().isoformat(),
        "description": "Multi-provider AI search attribution intelligence report.",
        "hasPart": [],
    }
    for r in results:
        entry = {
            "@type":      "SearchAction",
            "provider":   r.provider,
            "query":      r.query,
            "timestamp":  r.timestamp,
            "status":     r.status,
            "semanticScore": round(r.semantic_score, 4),
            "attributions": [
                {
                    "@type":  "WebPage",
                    "url":    a.url,
                    "name":   a.title,
                    "author": {"@type": "Person", "name": a.author},
                    "mentions": a.mention_count,
                }
                for a in r.attributions
            ],
        }
        doc["hasPart"].append(entry)
    try:
        Path(path).write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
        return True
    except Exception as e:
        print(f"[Export JSON-LD] {e}")
        return False


def export_pdf(results: list, path: str) -> bool:
    """Export PDF executive summary using ReportLab."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.colors import HexColor, white
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        )
        from reportlab.lib.enums import TA_CENTER, TA_LEFT

        W, H = A4
        doc  = SimpleDocTemplate(path, pagesize=A4, leftMargin=50, rightMargin=50,
                                  topMargin=60, bottomMargin=50)
        styles = getSampleStyleSheet()

        # Custom styles
        def style(name, **kw):
            s = ParagraphStyle(name, **kw)
            return s

        h1 = style("H1", fontSize=20, fontName="Helvetica-Bold",
                   textColor=HexColor("#00d4ff"), spaceAfter=6, alignment=TA_CENTER)
        h2 = style("H2", fontSize=13, fontName="Helvetica-Bold",
                   textColor=HexColor("#e2e8f0"), spaceBefore=14, spaceAfter=4)
        body = style("Body", fontSize=9, fontName="Helvetica",
                     textColor=HexColor("#8892a4"), spaceAfter=3, leading=14)
        kpi_s = style("KPI", fontSize=22, fontName="Helvetica-Bold",
                      textColor=HexColor("#00d4ff"), alignment=TA_CENTER)
        caption = style("Caption", fontSize=8, fontName="Helvetica",
                        textColor=HexColor("#4a5568"), alignment=TA_CENTER)

        BG  = HexColor("#0a0e17")
        CYN = HexColor("#00d4ff")
        DRK = HexColor("#141d2e")

        story = []

        # Header
        story.append(Spacer(1, 10))
        story.append(Paragraph("⬡ OMNI-ENGINE VISIBILITY REPORT", h1))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Developer: HSINI MOHAMED",
                               caption))
        story.append(HRFlowable(width="100%", thickness=1, color=CYN))
        story.append(Spacer(1, 12))

        # KPI summary table
        total_attr = sum(len(r.attributions) for r in results)
        domains    = len({a.domain for r in results for a in r.attributions})
        avg_sem    = (sum(r.semantic_score for r in results) / len(results)) if results else 0

        kpi_data = [
            [Paragraph("PROVIDERS", caption), Paragraph("ATTRIBUTIONS", caption),
             Paragraph("UNIQUE DOMAINS", caption), Paragraph("AVG SEMANTIC", caption)],
            [Paragraph(str(len(results)), kpi_s), Paragraph(str(total_attr), kpi_s),
             Paragraph(str(domains), kpi_s), Paragraph(f"{avg_sem:.2f}", kpi_s)],
        ]
        kpi_table = Table(kpi_data, colWidths=[W / 4 - 30] * 4)
        kpi_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), DRK),
            ("TEXTCOLOR",  (0, 0), (-1, -1), white),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [DRK, HexColor("#1a2540")]),
            ("BOX",        (0, 0), (-1, -1), 0.5, CYN),
            ("GRID",       (0, 0), (-1, -1), 0.3, HexColor("#1e3a5f")),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 16))

        # Per-provider sections
        for r in results:
            story.append(Paragraph(f"◈ {r.provider.upper()} — Score: {r.semantic_score:.2f} ({r.status.upper()})", h2))
            story.append(Paragraph(f"Query: {r.query}", body))
            story.append(Spacer(1, 4))

            if r.attributions:
                tdata = [["#", "Domain", "Title", "Author", "Mentions"]]
                for i, a in enumerate(r.attributions[:15], 1):
                    tdata.append([str(i), a.domain[:30], a.title[:40], a.author[:20], str(a.mention_count)])
                tbl = Table(tdata, colWidths=[25, 110, 160, 110, 60])
                tbl.setStyle(TableStyle([
                    ("BACKGROUND",    (0, 0), (-1, 0), HexColor("#003d4d")),
                    ("TEXTCOLOR",     (0, 0), (-1, 0), CYN),
                    ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE",      (0, 0), (-1, -1), 7.5),
                    ("ROWBACKGROUNDS",(0, 1), (-1, -1), [HexColor("#141d2e"), HexColor("#1a2540")]),
                    ("TEXTCOLOR",     (0, 1), (-1, -1), HexColor("#e2e8f0")),
                    ("GRID",          (0, 0), (-1, -1), 0.3, HexColor("#1e3a5f")),
                    ("TOPPADDING",    (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]))
                story.append(tbl)
            story.append(Spacer(1, 10))

        doc.build(story)
        return True
    except ImportError:
        # Fallback: plain text PDF-ish dump
        try:
            txt = f"OMNI-ENGINE VISIBILITY REPORT\n{datetime.now()}\n\n"
            for r in results:
                txt += f"{'='*60}\nProvider: {r.provider} | Score: {r.semantic_score:.2f}\n"
                for a in r.attributions:
                    txt += f"  • {a.domain} — {a.title} ({a.author})\n"
            Path(path.replace(".pdf", ".txt")).write_text(txt, encoding="utf-8")
            return True
        except Exception as e2:
            print(f"[Export fallback] {e2}")
            return False
    except Exception as e:
        print(f"[Export PDF] {e}")
        return False
