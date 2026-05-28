"""
PDF Report Generator
─────────────────────
Generates a professional 4–5 page PDF report using ReportLab.
Returns the PDF as bytes so Streamlit can offer a download button.
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

# ── Brand Colours ────────────────────────────────────────────────────
PURPLE      = colors.HexColor("#6366f1")
PURPLE_DARK = colors.HexColor("#4f46e5")
PURPLE_LIGHT= colors.HexColor("#a78bfa")
RED         = colors.HexColor("#ef4444")
AMBER       = colors.HexColor("#f59e0b")
GREEN       = colors.HexColor("#10b981")
DARK_BG     = colors.HexColor("#0f0c29")
DARK_CARD   = colors.HexColor("#1e1b4b")
WHITE       = colors.white
LIGHT_GRAY  = colors.HexColor("#e5e7eb")
MID_GRAY    = colors.HexColor("#9ca3af")
TEXT_DARK   = colors.HexColor("#1f2937")

PAGE_W, PAGE_H = A4
MARGIN = 2 * cm


# ── Helper: severity colour ──────────────────────────────────────────
def sev_color(severity: str) -> colors.Color:
    return RED if severity == "High" else AMBER


# ── Style sheet ──────────────────────────────────────────────────────
def _styles():
    base = getSampleStyleSheet()

    def add(name, **kwargs):
        base.add(ParagraphStyle(name=name, **kwargs))

    add("CoverTitle",
        fontSize=32, textColor=WHITE, alignment=TA_CENTER,
        fontName="Helvetica-Bold", spaceAfter=6)

    add("CoverSub",
        fontSize=13, textColor=PURPLE_LIGHT, alignment=TA_CENTER,
        fontName="Helvetica", spaceAfter=4)

    add("CoverMeta",
        fontSize=10, textColor=LIGHT_GRAY, alignment=TA_CENTER,
        fontName="Helvetica", spaceAfter=2)

    add("SectionTitle",
        fontSize=18, textColor=PURPLE, fontName="Helvetica-Bold",
        spaceBefore=14, spaceAfter=6)

    add("SubTitle",
        fontSize=13, textColor=TEXT_DARK, fontName="Helvetica-Bold",
        spaceBefore=8, spaceAfter=4)

    add("Body",
        fontSize=10, textColor=TEXT_DARK, fontName="Helvetica",
        leading=16, spaceAfter=6, alignment=TA_JUSTIFY)

    add("BulletItem",
        fontSize=10, textColor=TEXT_DARK, fontName="Helvetica",
        leading=15, leftIndent=14, spaceAfter=3)

    add("Label",
        fontSize=9, textColor=MID_GRAY, fontName="Helvetica",
        spaceAfter=2)

    add("MetricValue",
        fontSize=22, textColor=PURPLE, fontName="Helvetica-Bold",
        alignment=TA_CENTER, spaceAfter=2)

    add("MetricLabel",
        fontSize=8, textColor=MID_GRAY, fontName="Helvetica",
        alignment=TA_CENTER, spaceAfter=4)

    add("Footer",
        fontSize=8, textColor=MID_GRAY, fontName="Helvetica",
        alignment=TA_CENTER)

    add("ProblemTitle",
        fontSize=12, fontName="Helvetica-Bold",
        textColor=TEXT_DARK, spaceAfter=3)

    add("Explanation",
        fontSize=10.5, textColor=TEXT_DARK, fontName="Helvetica",
        leading=17, spaceAfter=8, alignment=TA_JUSTIFY)

    return base


# ── Cover Page ───────────────────────────────────────────────────────
def _cover_page(story, data: dict, health_score: int, n_problems: int, styles):
    # Full-page dark background drawn via table
    biz_name = data.get("business_name", "Your Business")
    biz_type = data.get("business_type", "E-Commerce")
    date_str = datetime.now().strftime("%B %d, %Y")
    health_label = (
        "🟢 Healthy" if health_score >= 70
        else "🟡 Needs Attention" if health_score >= 40
        else "🔴 Critical"
    )

    cover_data = [
        [Paragraph("", styles["CoverTitle"])],
        [Paragraph("🤖 AI Business Analyzer", styles["CoverTitle"])],
        [Spacer(1, 8)],
        [Paragraph("E-Commerce Strategy Report", styles["CoverSub"])],
        [Spacer(1, 20)],
        [Paragraph(f"<b>{biz_name}</b>", ParagraphStyle(
            "BizName", fontSize=26, textColor=WHITE,
            fontName="Helvetica-Bold", alignment=TA_CENTER))],
        [Paragraph(biz_type, styles["CoverMeta"])],
        [Spacer(1, 16)],
        [Paragraph(f"Business Health Score: <b>{health_score}/100</b> — {health_label}",
                   ParagraphStyle("HS", fontSize=12, textColor=PURPLE_LIGHT,
                                  fontName="Helvetica-Bold", alignment=TA_CENTER))],
        [Paragraph(f"{n_problems} Problem(s) Detected", styles["CoverMeta"])],
        [Spacer(1, 30)],
        [Paragraph(f"Generated on {date_str}", styles["CoverMeta"])],
        [Paragraph("Powered by AI Business Analyzer", styles["CoverMeta"])],
    ]

    cover_table = Table(cover_data, colWidths=[PAGE_W - 2 * MARGIN])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_BG),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 24),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 24),
        ("ROWBACKGROUNDS",(0, 0), (-1, -1), [DARK_BG]),
    ]))

    story.append(Spacer(1, 60))
    story.append(cover_table)
    story.append(PageBreak())


# ── Metrics Summary Table ────────────────────────────────────────────
def _metrics_table(story, data: dict, derived: dict, styles):
    story.append(Paragraph("📊 Business Snapshot", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=PURPLE_LIGHT, spaceAfter=10))

    metrics = [
        ("Monthly Sales",        f"₹{data.get('monthly_sales',0):,}",
                                 f"Target: ₹{data.get('monthly_target',0):,}"),
        ("Website Traffic",      f"{data.get('website_traffic',0):,} visitors",
                                 "Monthly unique visitors"),
        ("Conversion Rate",      f"{data.get('conversion_rate',0)}%",
                                 "Industry avg: 2.5%"),
        ("Marketing Spend",      f"₹{data.get('marketing_spend',0):,}",
                                 f"ROI: {derived.get('marketing_roi',0)}x"),
        ("Customer Retention",   f"{data.get('retention_rate',0)}%",
                                 "Target: ≥ 40%"),
        ("Inventory Level",      f"{data.get('inventory_level',0):,} units",
                                 f"Turnover: {derived.get('inventory_turnover',0)}x/mo"),
        ("Net Profit",           f"₹{derived.get('net_profit',0):,}",
                                 f"Margin: {derived.get('profit_margin',0)}%"),
        ("Avg Order Value",      f"₹{data.get('avg_order_value',0):,}",
                                 "Per transaction"),
    ]

    rows = []
    for i in range(0, len(metrics), 2):
        row = []
        for m in metrics[i:i+2]:
            cell = [
                Paragraph(m[0], styles["Label"]),
                Paragraph(m[1], styles["MetricValue"]),
                Paragraph(m[2], styles["MetricLabel"]),
            ]
            row.append(cell)
        if len(row) == 1:
            row.append("")  # padding
        rows.append(row)

    col_w = (PAGE_W - 2 * MARGIN - 10) / 2
    tbl = Table(rows, colWidths=[col_w, col_w])
    tbl.setStyle(TableStyle([
        ("BOX",         (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ("INNERGRID",   (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ("BACKGROUND",  (0, 0), (-1, -1), colors.HexColor("#f9fafb")),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 18))


# ── Problems Section ─────────────────────────────────────────────────
def _problems_section(story, problems: list, styles):
    story.append(Paragraph("❗ Problems Identified", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=RED, spaceAfter=10))

    if not problems:
        story.append(Paragraph(
            "✅ No major problems detected. Your business metrics are healthy.",
            styles["Body"]))
        story.append(Spacer(1, 10))
        return

    for i, prob in enumerate(problems, 1):
        color = sev_color(prob["severity"])

        rows = [
            [
                Paragraph(
                    f"<font color='#{color.hexval()[2:]}'>{prob['icon']} {i}. {prob['problem']}</font>",
                    styles["ProblemTitle"]),
                Paragraph(
                    f"<b>Severity:</b> {prob['severity']}  |  "
                    f"<b>Confidence:</b> {prob['confidence']}%",
                    ParagraphStyle("PS", fontSize=9, textColor=MID_GRAY,
                                   fontName="Helvetica", alignment=TA_RIGHT)),
            ],
            [
                Paragraph(prob.get("detail", ""), styles["Body"]),
                Paragraph(
                    f"Your value: <b>{prob['your_value']}</b><br/>"
                    f"Benchmark: <b>{prob['benchmark']}</b>",
                    ParagraphStyle("PVal", fontSize=9, textColor=TEXT_DARK,
                                   fontName="Helvetica", alignment=TA_RIGHT,
                                   leading=14)),
            ],
        ]

        tbl = Table(rows, colWidths=[PAGE_W - 2 * MARGIN - 130, 120])
        bg = colors.HexColor("#fff5f5") if prob["severity"] == "High" else colors.HexColor("#fffbeb")
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), bg),
            ("BOX",           (0, 0), (-1, -1), 1.5, color),
            ("TOPPADDING",    (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING",   (0, 0), (-1, 0), 12),
            ("RIGHTPADDING",  (-1, 0), (-1, -1), 12),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(KeepTogether([tbl, Spacer(1, 10)]))


# ── Strategies Section ───────────────────────────────────────────────
def _strategies_section(story, strategies: list, styles):
    story.append(PageBreak())
    story.append(Paragraph("✅ Recommended Strategies", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GREEN, spaceAfter=10))

    for strat in strategies:
        s = strat["strategies"]

        header_rows = [[
            Paragraph(
                f"{strat['icon']} {strat['problem']}",
                ParagraphStyle("SH", fontSize=13, fontName="Helvetica-Bold",
                               textColor=WHITE)),
            Paragraph(
                f"Confidence: {strat['confidence']}%",
                ParagraphStyle("SC", fontSize=10, fontName="Helvetica",
                               textColor=PURPLE_LIGHT, alignment=TA_RIGHT)),
        ]]
        header_tbl = Table(header_rows, colWidths=[PAGE_W - 2 * MARGIN - 120, 110])
        header_tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), DARK_CARD),
            ("TOPPADDING",    (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING",   (0, 0), (0, 0), 12),
            ("RIGHTPADDING",  (-1, 0), (-1, -1), 12),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ]))

        body_rows = []

        # Short-term
        qt_items = [Paragraph("⚡ Quick Wins (This Week)",
                              ParagraphStyle("QT", fontSize=11, fontName="Helvetica-Bold",
                                             textColor=AMBER, spaceAfter=4))]
        for item in s.get("short_term", []):
            qt_items.append(Paragraph(f"• {item}", styles["BulletItem"]))

        # Long-term
        lt_items = [Paragraph("🎯 Long-Term Strategy",
                              ParagraphStyle("LT", fontSize=11, fontName="Helvetica-Bold",
                                             textColor=GREEN, spaceAfter=4))]
        for item in s.get("long_term", []):
            lt_items.append(Paragraph(f"• {item}", styles["BulletItem"]))

        body_rows.append([qt_items, lt_items])

        # KPI + Tools row
        kpi_tools = Paragraph(
            f"<b>📌 KPI Target:</b> {s.get('kpi', '')}  |  "
            f"<b>🛠 Tools:</b> {', '.join(s.get('tools', []))}  |  "
            f"<b>Expected Impact:</b> {s.get('expected_impact', '')}",
            ParagraphStyle("KPITools", fontSize=9, textColor=MID_GRAY,
                           fontName="Helvetica", leading=13))
        body_rows.append([[kpi_tools], [""]])

        col_w = (PAGE_W - 2 * MARGIN) / 2
        body_tbl = Table(body_rows, colWidths=[col_w, col_w])
        body_tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor("#f9fafb")),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("SPAN",          (0, 1), (-1, 1)),
            ("LINEBELOW",     (0, 0), (-1, -2), 0.5, LIGHT_GRAY),
        ]))

        story.append(KeepTogether([header_tbl, body_tbl, Spacer(1, 16)]))


# ── Explanation Section ──────────────────────────────────────────────
def _explanation_section(story, explanation: str, styles):
    story.append(PageBreak())
    story.append(Paragraph("🧠 AI Analysis & Commentary", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=PURPLE_LIGHT, spaceAfter=10))

    expl_tbl = Table(
        [[Paragraph(explanation, styles["Explanation"])]],
        colWidths=[PAGE_W - 2 * MARGIN]
    )
    expl_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor("#f5f3ff")),
        ("LEFTPADDING",   (0, 0), (-1, -1), 16),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 16),
        ("TOPPADDING",    (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("BOX",           (0, 0), (-1, -1), 2, PURPLE),
    ]))
    story.append(expl_tbl)
    story.append(Spacer(1, 18))


# ── Action Plan Table ────────────────────────────────────────────────
def _action_plan(story, strategies: list, styles):
    story.append(Paragraph("📋 30-Day Action Plan", styles["SectionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=PURPLE_LIGHT, spaceAfter=10))

    header = [
        Paragraph("Week", ParagraphStyle("APH", fontSize=10, fontName="Helvetica-Bold",
                                         textColor=WHITE, alignment=TA_CENTER)),
        Paragraph("Action", ParagraphStyle("APH2", fontSize=10, fontName="Helvetica-Bold",
                                           textColor=WHITE)),
        Paragraph("Problem Addressed", ParagraphStyle("APH3", fontSize=10,
                                                       fontName="Helvetica-Bold",
                                                       textColor=WHITE)),
        Paragraph("Expected Result", ParagraphStyle("APH4", fontSize=10,
                                                     fontName="Helvetica-Bold",
                                                     textColor=WHITE)),
    ]

    rows = [header]
    week = 1
    for strat in strategies[:4]:  # top 4 problems
        for action in strat["strategies"].get("short_term", [])[:2]:
            rows.append([
                Paragraph(f"Week {week}", styles["Label"]),
                Paragraph(action, styles["Body"]),
                Paragraph(strat["problem"], styles["Label"]),
                Paragraph(strat["strategies"].get("expected_impact", "—"), styles["Label"]),
            ])
            week = min(week + 1, 4)

    col_ws = [45, PAGE_W - 2 * MARGIN - 45 - 130 - 100, 130, 100]
    tbl = Table(rows, colWidths=col_ws)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), PURPLE),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, colors.HexColor("#f9fafb")]),
        ("GRID",          (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 18))


# ── Footer on every page ─────────────────────────────────────────────
def _on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MID_GRAY)
    biz = getattr(doc, "_biz_name", "Business")
    date_str = datetime.now().strftime("%Y-%m-%d")
    canvas.drawString(MARGIN, 15 * mm,
                      f"AI Business Analyzer  |  {biz}  |  {date_str}")
    canvas.drawRightString(PAGE_W - MARGIN, 15 * mm, f"Page {doc.page}")
    canvas.restoreState()


# ── Main entry point ─────────────────────────────────────────────────
def generate_pdf(results: dict) -> bytes:
    """
    Takes the full results dict from app.py and returns PDF bytes.
    """
    data        = results["data"]
    problems    = results["problems"]
    strategies  = results["strategies"]
    explanation = results["explanation"]
    derived     = results["metrics"]

    # Health score
    score = 100 - sum(20 if p["severity"] == "High" else 10 for p in problems)
    health_score = max(10, score)

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN,  bottomMargin=2 * cm,
    )
    doc._biz_name = data.get("business_name", "Business")

    styles = _styles()
    story  = []

    # ── Pages ────────────────────────────────────────────────────────
    _cover_page(story, data, health_score, len(problems), styles)
    _metrics_table(story, data, derived, styles)
    _problems_section(story, problems, styles)
    _strategies_section(story, strategies, styles)
    _explanation_section(story, explanation, styles)
    _action_plan(story, strategies, styles)

    doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
    return buf.getvalue()


# ── PDFGenerator Class Wrapper ───────────────────────────────────────
class PDFGenerator:
    """Wrapper class for PDF generation functionality."""
    
    def generate_pdf(self, results: dict) -> bytes:
        """
        Generates a professional PDF report from analysis results.
        Returns the PDF as bytes for download.
        """
        return generate_pdf(results)
