from typing import Any, Dict, List
import streamlit as st
from frontend.components.score_display import display_overall_score, display_score_breakdown


def _render_list_section(title: str, items: List[str], item_class: str, icon: str) -> None:
    if not items:
        return
    bullets = "".join(
        f'<div class="cv-feedback-item {item_class}"><span>{icon}</span>{item}</div>'
        for item in items
    )
    st.markdown(f'<div class="cv-section-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(bullets, unsafe_allow_html=True)
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)


def _render_keyword_section(analysis: Dict[str, Any]) -> None:
    keywords = analysis.get("important_keywords") or []
    missing   = analysis.get("missing_keywords") or []
    if not keywords and not missing:
        return

    st.markdown('<div class="cv-section-title">🔑 Keywords</div>', unsafe_allow_html=True)
    kc1, kc2 = st.columns(2)

    with kc1:
        if keywords:
            pills = "".join(f'<span class="cv-keyword-pill">{k}</span>' for k in keywords)
            st.markdown(f"""
            <div style="margin-bottom:0.5rem;font-size:0.78rem;font-weight:700;
                        text-transform:uppercase;letter-spacing:0.07em;color:#9CA3AF;">Detected</div>
            <div class="cv-keyword-grid">{pills}</div>
            """, unsafe_allow_html=True)

    with kc2:
        if missing:
            pills = "".join(
                f'<span class="cv-keyword-pill" style="background:rgba(244,63,94,0.07);'
                f'color:#BE123C;border-color:rgba(244,63,94,0.25);">{k}</span>'
                for k in missing
            )
            st.markdown(f"""
            <div style="margin-bottom:0.5rem;font-size:0.78rem;font-weight:700;
                        text-transform:uppercase;letter-spacing:0.07em;color:#9CA3AF;">Missing / Add These</div>
            <div class="cv-keyword-grid">{pills}</div>
            """, unsafe_allow_html=True)


def _render_skill_validation(analysis: Dict[str, Any]) -> None:
    sv = analysis.get("skill_validation") or {}
    validated = sv.get("validated_skills") or []
    unvalidated = sv.get("unvalidated_skills") or []
    if not validated and not unvalidated:
        return

    st.markdown('<div class="cv-section-title">✅ Skill Validation</div>', unsafe_allow_html=True)
    sc1, sc2 = st.columns(2)

    with sc1:
        if validated:
            st.markdown('<div style="font-size:0.78rem;font-weight:700;text-transform:uppercase;'
                        'letter-spacing:0.07em;color:#9CA3AF;margin-bottom:0.5rem;">Backed by evidence</div>',
                        unsafe_allow_html=True)
            for skill in validated:
                st.markdown(f'<div class="cv-feedback-item cv-feedback-strength">✅ {skill}</div>',
                            unsafe_allow_html=True)

    with sc2:
        if unvalidated:
            st.markdown('<div style="font-size:0.78rem;font-weight:700;text-transform:uppercase;'
                        'letter-spacing:0.07em;color:#9CA3AF;margin-bottom:0.5rem;">Needs evidence</div>',
                        unsafe_allow_html=True)
            for skill in unvalidated:
                st.markdown(f'<div class="cv-feedback-item cv-feedback-issue">⚠ {skill}</div>',
                            unsafe_allow_html=True)


def _render_jd_section(analysis: Dict[str, Any]) -> None:
    jd = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")
    if not jd:
        return

    match_pct  = float(jd.get("match_percentage", 0))
    matched_kw = jd.get("matched_keywords") or []
    missing_kw = jd.get("missing_keywords") or []
    rec        = jd.get("recommendations") or []

    bar_class = "excellent" if match_pct >= 80 else ("good" if match_pct >= 60 else "poor")

    st.markdown('<div class="cv-section-title">🎯 Job Description Match</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0B0F1A,#1a1060);border-radius:14px;
                padding:1.5rem 1.75rem;margin-bottom:1.25rem;position:relative;overflow:hidden;">
        <div style="position:absolute;top:-40px;right:-40px;width:160px;height:160px;border-radius:50%;
                    background:radial-gradient(circle,rgba(99,102,241,0.3),transparent 70%);pointer-events:none;"></div>
        <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                    letter-spacing:0.1em;color:#64748B;margin-bottom:0.4rem;">Match Score</div>
        <div style="font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;
                    color:{'#34D399' if match_pct>=80 else '#FBBF24' if match_pct>=60 else '#FB7185'};
                    line-height:1;margin-bottom:0.75rem;">{match_pct:.0f}%</div>
        <div class="cv-progress-track" style="height:10px;">
            <div class="cv-progress-fill {bar_class}" style="width:{match_pct:.1f}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    jc1, jc2 = st.columns(2)
    with jc1:
        if matched_kw:
            pills = "".join(f'<span class="cv-keyword-pill">{k}</span>' for k in matched_kw)
            st.markdown(f'<div style="font-size:0.78rem;font-weight:700;text-transform:uppercase;'
                        f'letter-spacing:0.07em;color:#9CA3AF;margin-bottom:0.4rem;">Matched keywords</div>'
                        f'<div class="cv-keyword-grid">{pills}</div>', unsafe_allow_html=True)
    with jc2:
        if missing_kw:
            pills = "".join(
                f'<span class="cv-keyword-pill" style="background:rgba(244,63,94,0.07);'
                f'color:#BE123C;border-color:rgba(244,63,94,0.25);">{k}</span>'
                for k in missing_kw
            )
            st.markdown(f'<div style="font-size:0.78rem;font-weight:700;text-transform:uppercase;'
                        f'letter-spacing:0.07em;color:#9CA3AF;margin-bottom:0.4rem;">Missing keywords</div>'
                        f'<div class="cv-keyword-grid">{pills}</div>', unsafe_allow_html=True)

    if rec:
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        _render_list_section("💡 JD Recommendations", rec, "cv-feedback-tip", "->")


def display_results_dashboard(analysis: Dict[str, Any]) -> None:
    if not analysis:
        return

    st.markdown("---")

    # Overall score + breakdown
    display_overall_score(analysis)
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    display_score_breakdown(analysis)
    st.markdown("---")

    # Strengths & issues
    _render_list_section(
        "💪 Strengths",
        analysis.get("strengths") or [],
        "cv-feedback-strength", "✓"
    )
    _render_list_section(
        "🚨 Critical Issues",
        analysis.get("critical_issues") or [],
        "cv-feedback-issue", "✗"
    )
    _render_list_section(
        "💡 Suggestions",
        analysis.get("suggestions") or [],
        "cv-feedback-tip", "->"
    )

    # Keywords
    _render_keyword_section(analysis)

    # Skill validation
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    _render_skill_validation(analysis)

    # JD comparison
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    _render_jd_section(analysis)

    st.markdown("---")
