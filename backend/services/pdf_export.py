from __future__ import annotations

import logging
from io import BytesIO
from typing import Any, Dict, Iterable
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

logger = logging.getLogger("ats_resume_scorer")


# ============================================================
# Text helpers
# ============================================================

def _safe_text(value: Any) -> str:
    """
    Convert arbitrary values into safe ReportLab paragraph text.
    """

    if value is None:
        return ""

    text = str(value)

    replacements = {
        "\x00": "",
        "✅": "",
        "🌟": "",
        "❌": "",
        "⚠️": "",
        "⚠": "",
        "📝": "",
        "🔴": "",
        "🟡": "",
        "🟢": "",
        "🟠": "",
        "👍": "",
        "⚡": "",
        "🎯": "",
        "📊": "",
        "📥": "",
        "📄": "",
        "•": "-",
        "—": "-",
        "–": "-",
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "\r\n": "\n",
        "\r": "\n",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return escape(text.strip())


def _display_key(value: Any) -> str:
    """
    Convert snake_case keys into readable labels.
    """

    text = str(value).replace("_", " ").strip()

    return text.title()


def _as_list(value: Any) -> list[Any]:
    """
    Normalize arbitrary values into a list.
    """

    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    if isinstance(value, set):
        return list(value)

    return [value]


def _format_number(value: Any) -> str:
    """
    Format numeric values cleanly.
    """

    if value is None:
        return "N/A"

    if isinstance(value, float):
        return f"{value:.1f}"

    return str(value)


# ============================================================
# PDF styles
# ============================================================

def _build_styles():
    styles = getSampleStyleSheet()

    return {
        "title": ParagraphStyle(
            "CVInsightTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=21,
            leading=25,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#172554"),
            spaceAfter=7,
        ),

        "subtitle": ParagraphStyle(
            "CVInsightSubtitle",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#64748B"),
            spaceAfter=15,
        ),

        "heading": ParagraphStyle(
            "CVInsightHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=colors.HexColor("#1E3A8A"),
            spaceBefore=11,
            spaceAfter=7,
        ),

        "subheading": ParagraphStyle(
            "CVInsightSubheading",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor("#334155"),
            spaceBefore=7,
            spaceAfter=4,
        ),

        "body": ParagraphStyle(
            "CVInsightBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#1F2937"),
            spaceAfter=5,
        ),

        "bullet": ParagraphStyle(
            "CVInsightBullet",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            leftIndent=11,
            firstLineIndent=-7,
            textColor=colors.HexColor("#1F2937"),
            spaceAfter=4,
        ),

        "small": ParagraphStyle(
            "CVInsightSmall",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#64748B"),
            spaceAfter=3,
        ),
    }


# ============================================================
# Generic rendering helpers
# ============================================================

def _render_list(
    story: list,
    values: Iterable[Any],
    styles: dict,
) -> None:
    """
    Render list values safely.
    """

    for item in values:
        if item is None:
            continue

        if isinstance(item, dict):
            parts = []

            for key, value in item.items():
                if value in (None, "", [], {}):
                    continue

                parts.append(
                    f"<b>{_safe_text(_display_key(key))}:</b> "
                    f"{_safe_text(value)}"
                )

            if parts:
                story.append(
                    Paragraph(
                        "- " + " | ".join(parts),
                        styles["bullet"],
                    )
                )

        else:
            text = _safe_text(item)

            if text:
                story.append(
                    Paragraph(
                        f"- {text}",
                        styles["bullet"],
                    )
                )


def _render_dict(
    story: list,
    data: Dict[str, Any],
    styles: dict,
) -> None:
    """
    Render nested dictionaries.
    """

    for key, value in data.items():
        if value in (None, "", [], {}):
            continue

        label = _safe_text(_display_key(key))

        if isinstance(value, dict):
            story.append(
                Paragraph(
                    label,
                    styles["subheading"],
                )
            )

            _render_dict(
                story,
                value,
                styles,
            )

        elif isinstance(value, (list, tuple, set)):
            story.append(
                Paragraph(
                    label,
                    styles["subheading"],
                )
            )

            _render_list(
                story,
                value,
                styles,
            )

        else:
            story.append(
                Paragraph(
                    f"<b>{label}:</b> "
                    f"{_safe_text(value)}",
                    styles["body"],
                )
            )


# ============================================================
# PDF header/footer
# ============================================================

def _draw_page(canvas, doc):
    """
    Draw page number and footer.
    """

    canvas.saveState()

    width, _height = A4

    canvas.setFont(
        "Helvetica",
        7.5,
    )

    canvas.setFillColor(
        colors.HexColor("#64748B")
    )

    canvas.drawString(
        16 * mm,
        9 * mm,
        "CVInsight Pro - AI Resume Intelligence Report",
    )

    canvas.drawRightString(
        width - 16 * mm,
        9 * mm,
        f"Page {doc.page}",
    )

    canvas.restoreState()


# ============================================================
# Main analysis → PDF function
# ============================================================

def generate_pdf_from_analysis(
    analysis: Dict[str, Any],
) -> bytes:
    """
    Generate a PDF directly from AnalysisResponse.model_dump()
    or a stored analysis_result dictionary.

    Args:
        analysis:
            ATS analysis dictionary.

    Returns:
        PDF file content as bytes.
    """

    if not isinstance(analysis, dict):
        raise TypeError(
            "analysis must be a dictionary"
        )

    if not analysis:
        raise ValueError(
            "analysis cannot be empty"
        )

    logger.info(
        "Generating PDF from analysis data"
    )

    buffer = BytesIO()

    styles = _build_styles()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=15 * mm,
        bottomMargin=17 * mm,
        title="CVInsight Pro ATS Analysis Report",
        author="CVInsight Pro",
        subject="AI-powered ATS resume analysis",
    )

    story = []

    # --------------------------------------------------------
    # Report title
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "CVInsight Pro",
            styles["title"],
        )
    )

    story.append(
        Paragraph(
            "AI Resume Intelligence & ATS Compatibility Report",
            styles["subtitle"],
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=0.7,
            color=colors.HexColor("#CBD5E1"),
            spaceBefore=2,
            spaceAfter=12,
        )
    )

    # --------------------------------------------------------
    # ATS score
    # --------------------------------------------------------

    ats_score = analysis.get(
        "ATS_score",
        analysis.get(
            "ats_score",
            0,
        ),
    )

    score_text = _format_number(ats_score)

    score_table = Table(
        [
            [
                Paragraph(
                    "<b>Overall ATS Score</b>",
                    styles["body"],
                ),
                Paragraph(
                    f"<b>{_safe_text(score_text)} / 100</b>",
                    styles["body"],
                ),
            ]
        ],
        colWidths=[
            110 * mm,
            55 * mm,
        ],
    )

    score_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#EFF6FF"),
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    colors.HexColor("#BFDBFE"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
            ]
        )
    )

    story.append(score_table)
    story.append(Spacer(1, 10))

    # --------------------------------------------------------
    # Interpretation
    # --------------------------------------------------------

    interpretation = analysis.get(
        "interpretation"
    )

    if interpretation:
        story.append(
            Paragraph(
                "Executive Interpretation",
                styles["heading"],
            )
        )

        story.append(
            Paragraph(
                _safe_text(interpretation),
                styles["body"],
            )
        )

    # --------------------------------------------------------
    # Component scores
    # --------------------------------------------------------

    component_scores = analysis.get(
        "component_scores"
    ) or {}

    if component_scores:
        story.append(
            Paragraph(
                "Component Scores",
                styles["heading"],
            )
        )

        table_data = [
            [
                Paragraph(
                    "<b>Component</b>",
                    styles["body"],
                ),
                Paragraph(
                    "<b>Score</b>",
                    styles["body"],
                ),
            ]
        ]

        for key, value in component_scores.items():
            table_data.append(
                [
                    Paragraph(
                        _safe_text(
                            _display_key(key)
                        ),
                        styles["body"],
                    ),
                    Paragraph(
                        _safe_text(
                            _format_number(value)
                        ),
                        styles["body"],
                    ),
                ]
            )

        component_table = Table(
            table_data,
            colWidths=[
                120 * mm,
                45 * mm,
            ],
            repeatRows=1,
        )

        component_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#1E3A8A"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, -1),
                        colors.white,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.HexColor("#CBD5E1"),
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ]
            )
        )

        story.append(component_table)

    # --------------------------------------------------------
    # Issues summary
    # --------------------------------------------------------

    issues_summary = analysis.get(
        "issues_summary"
    )

    if issues_summary:
        story.append(
            Paragraph(
                "Issues Summary",
                styles["heading"],
            )
        )

        if isinstance(
            issues_summary,
            dict,
        ):
            _render_dict(
                story,
                issues_summary,
                styles,
            )

        elif isinstance(
            issues_summary,
            (list, tuple),
        ):
            _render_list(
                story,
                issues_summary,
                styles,
            )

        else:
            story.append(
                Paragraph(
                    _safe_text(issues_summary),
                    styles["body"],
                )
            )

    # --------------------------------------------------------
    # Detailed feedback
    # --------------------------------------------------------

    detailed_feedback = analysis.get(
        "detailed_feedback"
    ) or []

    if detailed_feedback:
        story.append(
            Paragraph(
                "Detailed Feedback",
                styles["heading"],
            )
        )

        _render_list(
            story,
            detailed_feedback,
            styles,
        )

    # --------------------------------------------------------
    # Skill validation
    # --------------------------------------------------------

    skill_validation = analysis.get(
        "skill_validation_details"
    ) or {}

    if skill_validation:
        story.append(
            Paragraph(
                "Skill Evidence Validation",
                styles["heading"],
            )
        )

        validated_count = skill_validation.get(
            "validated_count",
            0,
        )

        total = skill_validation.get(
            "total",
            0,
        )

        validation_pct = skill_validation.get(
            "validation_pct",
            0,
        )

        validation_table = Table(
            [
                [
                    "Validated",
                    "Total Skills",
                    "Evidence Rate",
                ],
                [
                    str(validated_count),
                    str(total),
                    f"{_format_number(validation_pct)}%",
                ],
            ],
            colWidths=[
                55 * mm,
                55 * mm,
                55 * mm,
            ],
        )

        validation_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#F1F5F9"),
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "ALIGN",
                        (0, 0),
                        (-1, -1),
                        "CENTER",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.HexColor("#CBD5E1"),
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                ]
            )
        )

        story.append(validation_table)
        story.append(Spacer(1, 7))

        validated = skill_validation.get(
            "validated"
        ) or []

        if validated:
            story.append(
                Paragraph(
                    "Validated Skills",
                    styles["subheading"],
                )
            )

            _render_list(
                story,
                validated,
                styles,
            )

        unvalidated = skill_validation.get(
            "unvalidated"
        ) or []

        if unvalidated:
            story.append(
                Paragraph(
                    "Skills Requiring Supporting Evidence",
                    styles["subheading"],
                )
            )

            _render_list(
                story,
                unvalidated,
                styles,
            )

    # --------------------------------------------------------
    # Matched skills
    # --------------------------------------------------------

    skills = analysis.get(
        "skills"
    ) or []

    if skills:
        story.append(
            Paragraph(
                "Detected Skills",
                styles["heading"],
            )
        )

        story.append(
            Paragraph(
                ", ".join(
                    _safe_text(skill)
                    for skill in skills
                ),
                styles["body"],
            )
        )

    # --------------------------------------------------------
    # JD comparison
    # --------------------------------------------------------

    jd_data = (
        analysis.get("jd_match_analysis")
        or analysis.get("jd_comparison")
        or {}
    )

    if jd_data:
        story.append(
            Paragraph(
                "Job Description Match Analysis",
                styles["heading"],
            )
        )

        match_percentage = jd_data.get(
            "match_percentage",
            analysis.get(
                "keyword_match",
                0,
            ),
        )

        semantic_similarity = jd_data.get(
            "semantic_similarity",
            0,
        )

        jd_table = Table(
            [
                [
                    "JD Match",
                    "Semantic Similarity",
                ],
                [
                    f"{_format_number(match_percentage)}%",
                    _format_number(
                        semantic_similarity
                    ),
                ],
            ],
            colWidths=[
                82.5 * mm,
                82.5 * mm,
            ],
        )

        jd_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#F1F5F9"),
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "ALIGN",
                        (0, 0),
                        (-1, -1),
                        "CENTER",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.HexColor("#CBD5E1"),
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                ]
            )
        )

        story.append(jd_table)
        story.append(Spacer(1, 7))

        matched_keywords = jd_data.get(
            "matched_keywords"
        ) or analysis.get(
            "matched_keywords"
        ) or []

        if matched_keywords:
            story.append(
                Paragraph(
                    "Matched Keywords",
                    styles["subheading"],
                )
            )

            _render_list(
                story,
                matched_keywords,
                styles,
            )

        missing_keywords = jd_data.get(
            "missing_keywords"
        ) or analysis.get(
            "missing_keywords"
        ) or []

        if missing_keywords:
            story.append(
                Paragraph(
                    "Missing Keywords",
                    styles["subheading"],
                )
            )

            _render_list(
                story,
                missing_keywords,
                styles,
            )

        skills_gap = jd_data.get(
            "skills_gap"
        ) or []

        if skills_gap:
            story.append(
                Paragraph(
                    "Skills Gap",
                    styles["subheading"],
                )
            )

            _render_list(
                story,
                skills_gap,
                styles,
            )

    # --------------------------------------------------------
    # Build final PDF
    # --------------------------------------------------------

    try:
        doc.build(
            story,
            onFirstPage=_draw_page,
            onLaterPages=_draw_page,
        )

        pdf_bytes = buffer.getvalue()

        if not pdf_bytes:
            raise RuntimeError(
                "Generated PDF is empty"
            )

        logger.info(
            "PDF generated successfully: %d bytes",
            len(pdf_bytes),
        )

        return pdf_bytes

    except Exception:
        logger.exception(
            "PDF generation failed"
        )
        raise

    finally:
        buffer.close()


# ============================================================
# Backward-compatible HTML docs function
# ============================================================

def generate_combined_pdf(
    html_docs: Dict[str, str],
) -> bytes:
    """
    Backward-compatible function.

    The old implementation expected HTML documents and used
    WeasyPrint. This implementation creates a simple PDF from
    the supplied HTML strings without native WeasyPrint
    dependencies.

    Note:
        HTML is treated as text content, not full CSS-rendered HTML.
    """

    if not isinstance(html_docs, dict):
        raise TypeError(
            "html_docs must be a dictionary"
        )

    if not html_docs:
        raise ValueError(
            "html_docs cannot be empty"
        )

    analysis = {
        "ATS_score": 0,
        "interpretation": (
            "Combined report generated from legacy report data."
        ),
        "detailed_feedback": [
            {
                "section": name,
                "content": html_content,
            }
            for name, html_content in html_docs.items()
        ],
    }

    return generate_pdf_from_analysis(
        analysis
    )