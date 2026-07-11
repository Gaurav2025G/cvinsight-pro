from typing import Optional
import requests
import streamlit as st
from frontend.services import api_client
from frontend.components.dashboard import display_results_dashboard


def _read_jd(jd_file, jd_text: str) -> str:
    if jd_text:
        return jd_text.strip()
    if jd_file is None:
        return ""
    if jd_file.name.lower().endswith(".txt"):
        return jd_file.getvalue().decode("utf-8", errors="ignore")
    st.warning("Job description files must be `.txt`. Paste the text instead for PDF/DOCX.")
    return ""


def _show_backend_error(exc: Exception) -> None:
    if isinstance(exc, requests.ConnectionError):
        st.error("⚠ Cannot reach the backend. Is `uvicorn backend.main:app` running on port 8000?")
    elif isinstance(exc, requests.Timeout):
        st.error("[timer] The backend took too long. Try a smaller file or check server logs.")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        try:
            detail = exc.response.json().get("detail", exc.response.text)
        except ValueError:
            detail = exc.response.text
        st.error(f"Backend error {exc.response.status_code}: {detail}")
    else:
        st.error(f"Unexpected error: {exc}")


def _summary_text(analysis: dict) -> str:
    score = analysis.get("ATS_score", analysis.get("ats_score", 0))
    lines = [f"ATS Score: {score:.0f}/100", ""]
    if analysis.get("strengths"):
        lines.append("STRENGTHS:")
        lines.extend(f"  - {s}" for s in analysis["strengths"])
        lines.append("")
    if analysis.get("critical_issues"):
        lines.append("CRITICAL ISSUES:")
        lines.extend(f"  - {s}" for s in analysis["critical_issues"])
        lines.append("")
    if analysis.get("suggestions"):
        lines.append("SUGGESTIONS:")
        lines.extend(f"  - {s}" for s in analysis["suggestions"])
    return "\n".join(lines)


def _render_upload_area(analysis_mode: str):
    left, right = st.columns(2)

    with left:
        st.markdown("""
        <div style="font-weight:700;font-size:0.95rem;color:#111827;margin-bottom:0.6rem;">
            📄 Resume
        </div>
        """, unsafe_allow_html=True)
        resume_file = st.file_uploader(
            "Choose your resume file",
            type=["pdf", "doc", "docx"],
            help="PDF, DOC, or DOCX - max 5 MB",
            key="resume_upload",
            label_visibility="collapsed",
        )
        if resume_file:
            st.markdown(f"""
            <div class="cv-feedback-item cv-feedback-strength" style="margin-top:0.4rem;">
                ✅ <strong>{resume_file.name}</strong> &nbsp;&middot;&nbsp; {resume_file.size/1024:.1f} KB
            </div>
            """, unsafe_allow_html=True)

    jd_file: Optional[object] = None
    jd_text = ""

    with right:
        if analysis_mode == "Job Description Comparison":
            st.markdown("""
            <div style="font-weight:700;font-size:0.95rem;color:#111827;margin-bottom:0.6rem;">
                📋 Job Description
            </div>
            """, unsafe_allow_html=True)
            jd_method = st.radio(
                "Input method:",
                ["Paste Text", "Upload .txt File"],
                horizontal=True,
                key="jd_input_method",
                label_visibility="collapsed",
            )
            if jd_method == "Upload .txt File":
                jd_file = st.file_uploader(
                    "Choose JD file (.txt only)",
                    type=["txt"],
                    key="jd_upload",
                    label_visibility="collapsed",
                )
                if jd_file:
                    st.markdown(f'<div class="cv-feedback-item cv-feedback-strength">✅ {jd_file.name}</div>',
                                unsafe_allow_html=True)
            else:
                jd_text = st.text_area(
                    "Paste job description text:",
                    height=160,
                    placeholder="Paste the job description here...",
                    key="jd_text",
                    label_visibility="collapsed",
                )
                if jd_text:
                    st.markdown(f'<div class="cv-feedback-item cv-feedback-strength">✅ {len(jd_text):,} characters</div>',
                                unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="font-weight:700;font-size:0.95rem;color:#111827;margin-bottom:0.6rem;">
                📋 Job Description
            </div>
            <div class="cv-mode-info">
                Switch to <strong>Job Description Comparison</strong> mode to score against a specific role.
            </div>
            """, unsafe_allow_html=True)

    return resume_file, jd_file, jd_text


def _render_export_buttons(analysis: dict) -> None:
    st.markdown('<div class="cv-section-title">📥 Export Results</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        if st.button("📑 Generate PDF Report", use_container_width=True, type="primary"):
            try:
                with st.spinner("Generating PDF…"):
                    pdf_bytes = api_client.generate_pdf(
                        analysis,
                        access_token=st.session_state.get("access_token"),
                    )
                st.session_state["scorer_pdf_bytes"] = pdf_bytes
                st.success("✅ PDF ready — click Download below!")
            except requests.RequestException as exc:
                _show_backend_error(exc)
            except Exception as exc:
                st.error(f"PDF error: {exc}")

        if "scorer_pdf_bytes" in st.session_state:
            st.download_button(
                " Download PDF",
                data=st.session_state["scorer_pdf_bytes"],
                file_name="cvinsight_report.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="download_pdf_report",
            )

    with c2:
        st.download_button(
            "📄 Download Summary (.txt)",
            data=_summary_text(analysis),
            file_name="cvinsight_summary.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_summary",
        )


def render() -> None:
    # -- PAGE HEADER ---------------------------------------------------
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div class="cv-hero-eyebrow">Resume Scanner</div>
        <h1 style="font-family:'Syne',sans-serif;font-size:1.9rem;font-weight:800;color:#111827;margin:0.4rem 0 0.4rem;">
            ATS Resume Scorer
        </h1>
        <p style="color:#6B7280;font-size:0.9rem;margin:0;">
            Upload your resume - and optionally a job description - for a full AI-powered analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # -- MODE SELECTOR -------------------------------------------------
    analysis_mode = st.radio(
        "Analysis mode:",
        ["General ATS Score", "Job Description Comparison"],
        horizontal=True,
        help="General: scores your resume on its own. JD Comparison: scores it against a specific role.",
    )

    st.markdown("<div style='height:0.25rem'></div>", unsafe_allow_html=True)

    if analysis_mode == "Job Description Comparison":
        st.markdown("""
        <div class="cv-mode-info">
            🎯 <strong>JD mode active</strong> - paste or upload the job description on the right.
            Your score will reflect how well your resume matches this specific role.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # -- UPLOAD AREA ---------------------------------------------------
    resume_file, jd_file, jd_text = _render_upload_area(analysis_mode)

    st.markdown("---")

    # -- AUTH (optional — analysis works without login) ----------------
    access_token = st.session_state.get("access_token")
    if not access_token:
        st.markdown("""
        <div class="cv-feedback-item cv-feedback-tip">
            💡 <strong>Tip:</strong> Sign in to save your results to history. Analysis works without an account.
        </div>
        """, unsafe_allow_html=True)

    # -- ANALYZE BUTTON ------------------------------------------------
    if not resume_file:
        st.markdown("""
        <div style="text-align:center;padding:2rem;background:#F8FAFF;
                    border:1px dashed #C7D2FE;border-radius:12px;color:#6B7280;font-size:0.9rem;">
            👆 Upload your resume above to begin.
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.get("scorer_analysis"):
            display_results_dashboard(st.session_state["scorer_analysis"])
        return

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        analyze = st.button("🚀  Analyze My Resume", use_container_width=True, type="primary")

    if not analyze:
        if st.session_state.get("scorer_analysis"):
            st.markdown("<br>", unsafe_allow_html=True)
            display_results_dashboard(st.session_state["scorer_analysis"])
            _render_export_buttons(st.session_state["scorer_analysis"])
        return

    # -- RUN ANALYSIS --------------------------------------------------
    st.session_state.pop("scorer_pdf_bytes", None)
    st.session_state.pop("scorer_analysis", None)

    job_description = (
        _read_jd(jd_file, jd_text) if analysis_mode == "Job Description Comparison" else ""
    )

    try:
        with st.spinner("Analyzing your resume - this takes 10-30 seconds..."):
            analysis = api_client.analyze_resume(
                resume_file=resume_file,
                access_token=access_token,
                job_description=job_description,
            )
    except requests.RequestException as exc:
        _show_backend_error(exc)
        return

    st.session_state["scorer_analysis"] = analysis
    st.markdown("""
    <div class="cv-feedback-item cv-feedback-strength" style="margin-bottom:1rem;">
        ✅ <strong>Analysis complete!</strong> Scroll down to see your results.
    </div>
    """, unsafe_allow_html=True)
    display_results_dashboard(analysis)
    _render_export_buttons(analysis)