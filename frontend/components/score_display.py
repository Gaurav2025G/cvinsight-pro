from typing import Any, Dict
import streamlit as st
from frontend.components._helpers import get_score_color, get_score_emoji

COMPONENTS = [
    ("Formatting",        "formatting",        20, "📝"),
    ("Keywords & Skills", "keywords",          25, "🔑"),
    ("Content Quality",   "content",           25, "📄"),
    ("Skill Validation",  "skill_validation",  15, "✅"),
    ("ATS Compatibility", "ats_compatibility", 15, "🤖"),
]


def display_overall_score(analysis: Dict[str, Any]) -> None:
    score = float(analysis.get("ATS_score", analysis.get("ats_score", 0)))
    interpretation = analysis.get("interpretation", "")
    emoji = get_score_emoji(score)

    if score >= 80:
        score_class = "cv-score-excellent"
    elif score >= 60:
        score_class = "cv-score-good"
    else:
        score_class = "cv-score-poor"

    st.markdown('<div class="cv-section-title">📊 Analysis Results</div>', unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown(f"""
        <div class="cv-score-card">
            <div class="cv-score-label">Overall ATS Score</div>
            <div class="cv-score-number {score_class}">{emoji} {score:.0f}</div>
            <div class="cv-score-label" style="margin-top:0.5rem;">out of 100</div>
            <div class="cv-score-interp" style="margin-top:0.6rem;">{interpretation}</div>
        </div>
        """, unsafe_allow_html=True)


def display_score_breakdown(analysis: Dict[str, Any]) -> None:
    cs = analysis.get("component_scores") or {}
    st.markdown('<div class="cv-section-title">📈 Score Breakdown</div>', unsafe_allow_html=True)

    left, right = st.columns(2)
    for i, (label, key, max_score, icon) in enumerate(COMPONENTS):
        value = float(cs.get(key, 0))
        pct   = (value / max_score * 100) if max_score else 0
        bar_class = "excellent" if pct >= 80 else ("good" if pct >= 60 else "poor")
        col = left if i % 2 == 0 else right

        with col:
            st.markdown(f"""
            <div class="cv-progress-row">
                <div class="cv-progress-header">
                    <span class="cv-progress-label">{icon} {label}</span>
                    <span class="cv-progress-value">{value:.0f}/{max_score}</span>
                </div>
                <div class="cv-progress-track">
                    <div class="cv-progress-fill {bar_class}" style="width:{pct:.1f}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
