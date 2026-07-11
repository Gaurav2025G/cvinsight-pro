import streamlit as st


def render():
    # -- HERO --------------------------------------------------------
    st.markdown("""
    <div class="cv-hero">
        <div class="cv-hero-eyebrow">AI-Powered Resume Intelligence</div>
        <h1>Get Hired Faster with<br>a Smarter Resume</h1>
        <p class="cv-hero-sub">
            CVInsight scans your resume the same way ATS software does -
            scoring it across 5 dimensions and surfacing exactly what to fix
            before a recruiter ever sees it.
        </p>
        <div class="cv-hero-badge">✦ Trusted by 10,000+ job seekers</div>
    </div>
    """, unsafe_allow_html=True)

    # -- CTA BUTTON --------------------------------------------------
    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:
        if st.button("Analyze My Resume  ->", use_container_width=True, type="primary"):
            st.session_state.current_view = 'scorer'
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # -- STATS ROW ---------------------------------------------------
    st.markdown("""
    <div class="cv-stat-grid">
        <div class="cv-stat-item">
            <span class="val">98%</span>
            <span class="lbl">ATS Coverage</span>
        </div>
        <div class="cv-stat-item">
            <span class="val">&lt;30s</span>
            <span class="lbl">Analysis Time</span>
        </div>
        <div class="cv-stat-item">
            <span class="val">5 Dims</span>
            <span class="lbl">Scored</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -- FEATURES ----------------------------------------------------
    st.markdown('<div class="cv-section-title">✦ What CVInsight checks</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    features = [
        ("📊", "Comprehensive Scoring",
         "Scored across Formatting, Keywords, Content Quality, Skill Validation, and ATS Compatibility - every dimension that matters."),
        ("🔍", "AI Skill Validation",
         "Your claimed skills are cross-checked against your actual project descriptions using semantic analysis. No more empty claims."),
        ("🔒", "Private by Design",
         "All processing happens on your own server. Your resume never leaves your infrastructure - 100% private."),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3], features):
        with col:
            st.markdown(f"""
            <div class="cv-feature-card">
                <span class="cv-feature-icon">{icon}</span>
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -- HOW IT WORKS -------------------------------------------------
    st.markdown('<div class="cv-section-title">🚀 How it works</div>', unsafe_allow_html=True)

    steps = [
        ("1", "Upload your resume", "PDF, DOC, or DOCX - up to 5 MB."),
        ("2", "Add a job description (optional)", "Paste or upload the role's JD for a targeted match score."),
        ("3", "Get your report", "Scores, critical issues, skill gaps, and ranked action items - in under 30 seconds."),
    ]
    s1, s2, s3 = st.columns(3)
    for col, (num, title, desc) in zip([s1, s2, s3], steps):
        with col:
            st.markdown(f"""
            <div class="cv-step">
                <div class="cv-step-number">{num}</div>
                <div class="cv-step-content">
                    <h4>{title}</h4>
                    <p>{desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -- SCORE BREAKDOWN PREVIEW --------------------------------------
    st.markdown('<div class="cv-section-title">📈 Scoring dimensions</div>', unsafe_allow_html=True)
    dimensions = [
        ("📝 Formatting", 20, "Structure, section headers, whitespace, readability."),
        ("🔑 Keywords & Skills", 25, "Role-relevant terms and technology stack match."),
        ("📄 Content Quality", 25, "Clarity, impact, quantified achievements."),
        ("✅ Skill Validation", 15, "Claimed skills backed by real project evidence."),
        ("🤖 ATS Compatibility", 15, "Parse-ability by automated screening software."),
    ]
    dc1, dc2 = st.columns(2)
    for i, (label, weight, desc) in enumerate(dimensions):
        col = dc1 if i % 2 == 0 else dc2
        with col:
            st.markdown(f"""
            <div style="margin-bottom:1rem;">
                <div class="cv-progress-header">
                    <span class="cv-progress-label">{label}</span>
                    <span class="cv-tag cv-tag-indigo">{weight} pts</span>
                </div>
                <div style="font-size:0.8rem;color:var(--text-muted);margin-bottom:0.35rem;">{desc}</div>
                <div class="cv-progress-track">
                    <div class="cv-progress-fill excellent" style="width:{weight*4}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -- BOTTOM CTA ---------------------------------------------------
    st.markdown("""
    <div style="text-align:center; padding:2.5rem 1rem; background:linear-gradient(135deg,#EEF2FF,#F8FAFF);
                border-radius:16px; border:1px solid #E0E7FF;">
        <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;color:#111827;margin-bottom:0.5rem;">
            Ready to optimize your resume?
        </div>
        <div style="font-size:0.9rem;color:#6B7280;margin-bottom:1.25rem;">
            Free to use. No account required for a quick preview.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        if st.button("Get My ATS Score  ->", use_container_width=True, type="primary", key="cta_bottom"):
            st.session_state.current_view = 'scorer'
            st.rerun()
