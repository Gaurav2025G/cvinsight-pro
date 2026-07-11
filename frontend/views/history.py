import requests
import streamlit as st
from frontend.services import api_client


def _show_backend_error(exc: Exception) -> None:
    if isinstance(exc, requests.ConnectionError):
        st.error("Could not reach the backend. Is it running on port 8000?")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        st.error(f"Backend returned {exc.response.status_code}: {exc.response.text}")
    else:
        st.error(f"Unexpected error: {exc}")


def _score_color(score: float) -> str:
    if score >= 80: return "#10B981"
    if score >= 60: return "#F59E0B"
    return "#F43F5E"


def _score_label(score: float) -> str:
    if score >= 90: return "Excellent"
    if score >= 75: return "Good"
    if score >= 60: return "Fair"
    return "Needs Work"


def render() -> None:
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div class="cv-hero-eyebrow">Your Account</div>
        <h1 style="font-family:'Syne',sans-serif;font-size:1.9rem;font-weight:800;color:#111827;margin:0.4rem 0 0.4rem;">
            Analysis History
        </h1>
        <p style="color:#6B7280;font-size:0.9rem;margin:0;">All resume scans saved to your account.</p>
    </div>
    """, unsafe_allow_html=True)

    access_token = st.session_state.get("access_token")
    if not access_token:
        st.markdown("""
        <div style="text-align:center;padding:3rem 2rem;background:#F8FAFF;
                    border:1px solid #E0E7FF;border-radius:16px;">
            <div style="font-size:2.5rem;margin-bottom:0.75rem;">🔐</div>
            <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;
                        color:#111827;margin-bottom:0.4rem;">Sign in to see your history</div>
            <p style="color:#6B7280;font-size:0.875rem;">Your analyses are saved securely to your account.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    try:
        history = api_client.get_history(access_token)
    except requests.RequestException as exc:
        _show_backend_error(exc)
        return

    if not history:
        st.markdown("""
        <div style="text-align:center;padding:3rem 2rem;background:#F8FAFF;
                    border:1px dashed #C7D2FE;border-radius:16px;">
            <div style="font-size:2.5rem;margin-bottom:0.75rem;">📭</div>
            <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;
                        color:#111827;margin-bottom:0.4rem;">No analyses yet</div>
            <p style="color:#6B7280;font-size:0.875rem;">
                Run your first resume scan to start building your history.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1.2, 1])
        with col2:
            if st.button("Analyze My Resume  ->", use_container_width=True, type="primary"):
                st.session_state.current_view = "scorer"
                st.rerun()
        return

    # -- SUMMARY BAR --------------------------------------------------
    scores = [float(e.get("ats_score", 0)) for e in history]
    avg = sum(scores) / len(scores) if scores else 0
    best = max(scores) if scores else 0

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Scans", len(history))
    with m2:
        st.metric("Average Score", f"{avg:.0f}/100")
    with m3:
        st.metric("Best Score", f"{best:.0f}/100")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="cv-section-title">📄 {len(history)} saved {"analysis" if len(history)==1 else "analyses"}</div>', unsafe_allow_html=True)

    # -- HISTORY ITEMS -------------------------------------------------
    for idx, entry in enumerate(history):
        filename  = entry.get("filename", "resume")
        ats_score = float(entry.get("ats_score", 0))
        created   = entry.get("created_at", "")[:10] if entry.get("created_at") else "-"
        analysis  = entry.get("analysis_result") or {}
        cs        = analysis.get("component_scores") or {}
        jd        = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")
        color     = _score_color(ats_score)
        label     = _score_label(ats_score)
        entry_id  = entry.get("id")

        with st.expander(f"📄  {filename}   ·   {ats_score:.0f}/100   ·   {created}"):
            # Score badge + label
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.25rem;">
                <div style="font-family:'Syne',sans-serif;font-size:2.8rem;font-weight:800;color:{color};line-height:1;">
                    {ats_score:.0f}
                </div>
                <div>
                    <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;color:#9CA3AF;font-weight:600;">ATS Score</div>
                    <div style="font-size:0.85rem;font-weight:700;color:{color};">{label}</div>
                </div>
                {f'<span class="cv-tag cv-tag-green" style="margin-left:auto;">JD Match: {jd.get("match_percentage",0):.0f}%</span>' if jd else ''}
            </div>
            """, unsafe_allow_html=True)

            # Component breakdown
            components = [
                ("📝 Formatting",        cs.get("formatting", 0),        20),
                ("🔑 Keywords",          cs.get("keywords", 0),          25),
                ("📄 Content",           cs.get("content", 0),           25),
                ("✅ Skill Validation",  cs.get("skill_validation", 0),  15),
                ("🤖 ATS Compat.",       cs.get("ats_compatibility", 0), 15),
            ]
            cc1, cc2 = st.columns(2)
            for i, (lbl, val, mx) in enumerate(components):
                pct = (val / mx * 100) if mx else 0
                bar_class = "excellent" if pct >= 80 else ("good" if pct >= 60 else "poor")
                col = cc1 if i % 2 == 0 else cc2
                with col:
                    st.markdown(f"""
                    <div class="cv-progress-row">
                        <div class="cv-progress-header">
                            <span class="cv-progress-label">{lbl}</span>
                            <span class="cv-progress-value">{val:.0f}/{mx}</span>
                        </div>
                        <div class="cv-progress-track">
                            <div class="cv-progress-fill {bar_class}" style="width:{pct:.1f}%;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # Delete button
            if entry_id:
                st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
                dcol1, dcol2, dcol3 = st.columns([3, 1, 1])
                with dcol3:
                    if st.button("🗑️ Delete", key=f"delete_{idx}", use_container_width=True):
                        try:
                            api_client.delete_history_entry(str(entry_id), access_token)
                            st.success("Deleted.")
                            st.rerun()
                        except requests.RequestException as exc:
                            _show_backend_error(exc)
