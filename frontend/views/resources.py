import streamlit as st


def render():
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div class="cv-hero-eyebrow">Knowledge Base</div>
        <h1 style="font-family:'Syne',sans-serif;font-size:1.9rem;font-weight:800;color:#111827;margin:0.4rem 0 0.5rem;">
            ATS Optimization Guide
        </h1>
        <p style="color:#6B7280;font-size:0.95rem;margin:0;">
            Everything you need to pass automated screening and land the interview.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # -- DO's AND DON'Ts ----------------------------------------------
    st.markdown('<div class="cv-section-title">🎯 Quick Rules</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        dos = [
            ("✅", "Use standard section headings (Experience, Education, Skills)"),
            ("✅", "Mirror keywords from the job description exactly"),
            ("✅", "Quantify achievements - numbers stand out"),
            ("✅", "Use common fonts: Arial, Calibri, Times New Roman"),
            ("✅", "Save as PDF or DOCX"),
            ("✅", "Keep to 1-2 pages for under 10 years of experience"),
        ]
        items = "".join(f'<li><span>{icon}</span>{text}</li>' for icon, text in dos)
        st.markdown(f"""
        <div class="cv-tip-card">
            <h3 style="color:#059669;">Do these</h3>
            <ul class="cv-tip-list">{items}</ul>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        donts = [
            ("❌", "Tables, text boxes, or multi-column layouts"),
            ("❌", "Headers/footers for important contact info"),
            ("❌", "Images, logos, or icons"),
            ("❌", "Unusual or decorative fonts"),
            ("❌", "Keyword stuffing - ATS flags it"),
            ("❌", "Unexplained abbreviations on first use"),
        ]
        items = "".join(f'<li><span>{icon}</span>{text}</li>' for icon, text in donts)
        st.markdown(f"""
        <div class="cv-tip-card">
            <h3 style="color:#BE123C;">Avoid these</h3>
            <ul class="cv-tip-list">{items}</ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -- KEYWORDS BY INDUSTRY -----------------------------------------
    st.markdown('<div class="cv-section-title">🔑 High-Impact Keywords by Industry</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["💻 Tech", "💼 Business", "🎨 Creative", "🏥 Healthcare"])

    keyword_data = {
        "💻 Tech": {
            "Software Dev": ["Python", "JavaScript", "TypeScript", "React", "Node.js", "Django", "REST API", "Docker", "Kubernetes", "CI/CD", "Git", "AWS"],
            "Data & ML": ["Machine Learning", "TensorFlow", "PyTorch", "SQL", "Pandas", "Feature Engineering", "A/B Testing", "Data Pipeline"],
            "DevOps": ["Terraform", "Ansible", "Jenkins", "Linux", "Monitoring", "SRE", "Infrastructure as Code"],
        },
        "💼 Business": {
            "Management": ["Strategic Planning", "Stakeholder Management", "Budget Management", "OKRs", "Team Leadership", "Cross-functional"],
            "Finance": ["Financial Modeling", "Forecasting", "Variance Analysis", "GAAP", "Excel", "Power BI"],
            "Operations": ["Process Improvement", "Six Sigma", "Supply Chain", "KPI Tracking", "SOP Development"],
        },
        "🎨 Creative": {
            "Design": ["Figma", "Adobe XD", "UI/UX", "Wireframing", "Prototyping", "Design Systems", "Accessibility"],
            "Marketing": ["SEO/SEM", "Google Analytics", "Content Strategy", "Brand Identity", "Campaign Management"],
            "Video/Media": ["Premiere Pro", "After Effects", "Motion Graphics", "Color Grading", "Storyboarding"],
        },
        "🏥 Healthcare": {
            "Clinical": ["Patient Care", "EHR/EMR", "HIPAA Compliance", "Clinical Documentation", "Care Coordination"],
            "Admin": ["Medical Billing", "ICD-10", "CPT Codes", "Revenue Cycle", "JCAHO Standards"],
            "Research": ["IRB Protocol", "Clinical Trials", "Data Collection", "SPSS", "Regulatory Compliance"],
        },
    }

    for tab, (industry, subcats) in zip([tab1, tab2, tab3, tab4], keyword_data.items()):
        with tab:
            for subcat, keywords in subcats.items():
                pills = "".join(f'<span class="cv-keyword-pill">{kw}</span>' for kw in keywords)
                st.markdown(f"""
                <div style="margin-bottom:1.25rem;">
                    <div style="font-size:0.8rem;font-weight:700;text-transform:uppercase;
                                letter-spacing:0.07em;color:#9CA3AF;margin-bottom:0.5rem;">{subcat}</div>
                    <div class="cv-keyword-grid">{pills}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -- ATS SCORING BREAKDOWN ----------------------------------------
    st.markdown('<div class="cv-section-title">📊 How CVInsight Scores Your Resume</div>', unsafe_allow_html=True)

    scoring_info = [
        ("📝", "Formatting", "20 pts", "Section headers, bullet consistency, date formatting, whitespace, and overall readability.", "#6366F1"),
        ("🔑", "Keywords & Skills", "25 pts", "Presence of role-relevant terms, technical stack alignment, and keyword density balance.", "#14B8A6"),
        ("📄", "Content Quality", "25 pts", "Action verb usage, quantified impact, specificity of accomplishments, and narrative clarity.", "#F59E0B"),
        ("✅", "Skill Validation", "15 pts", "AI cross-references claimed skills against project descriptions and experience bullets.", "#10B981"),
        ("🤖", "ATS Compatibility", "15 pts", "File format, font safety, absence of tables/images/text-boxes, parse-ability score.", "#F43F5E"),
    ]

    for icon, name, pts, desc, color in scoring_info:
        st.markdown(f"""
        <div style="display:flex;gap:1rem;padding:1rem 1.25rem;background:#FFFFFF;
                    border:1px solid #E5E7EB;border-radius:12px;margin-bottom:0.6rem;
                    border-left:4px solid {color};box-shadow:0 1px 3px rgba(0,0,0,0.05);">
            <div style="font-size:1.5rem;flex-shrink:0;">{icon}</div>
            <div style="flex:1;">
                <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.25rem;">
                    <span style="font-weight:700;font-size:0.95rem;color:#111827;">{name}</span>
                    <span class="cv-tag cv-tag-indigo">{pts}</span>
                </div>
                <p style="font-size:0.85rem;color:#6B7280;margin:0;">{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -- SCORE INTERPRETATION -----------------------------------------
    st.markdown('<div class="cv-section-title">🏆 Score Interpretation</div>', unsafe_allow_html=True)

    ranges = [
        ("90-100", "Excellent", "#10B981", "rgba(16,185,129,0.08)", "Strong ATS pass. Focus on tailoring to specific roles."),
        ("75-89",  "Good",      "#F59E0B", "rgba(245,158,11,0.08)",  "Likely to pass. Address flagged issues for a higher match rate."),
        ("60-74",  "Fair",      "#F97316", "rgba(249,115,22,0.08)",  "May get filtered. Targeted improvements will make a real difference."),
        ("0-59",   "Needs Work","#F43F5E", "rgba(244,63,94,0.08)",   "High risk of rejection. Follow the action items closely."),
    ]

    rc1, rc2 = st.columns(2)
    for i, (rng, label, color, bg, desc) in enumerate(ranges):
        col = rc1 if i % 2 == 0 else rc2
        with col:
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {color}33;border-radius:12px;
                        padding:1rem 1.25rem;margin-bottom:0.75rem;">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.3rem;">
                    <span style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;color:{color};">{rng}</span>
                    <span style="font-size:0.78rem;font-weight:700;color:{color};text-transform:uppercase;letter-spacing:0.06em;">{label}</span>
                </div>
                <p style="font-size:0.83rem;color:#6B7280;margin:0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -- CTA ----------------------------------------------------------
    st.markdown("""
    <div style="text-align:center;padding:2rem;background:linear-gradient(135deg,#EEF2FF,#F8FAFF);
                border-radius:16px;border:1px solid #E0E7FF;">
        <div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:800;color:#111827;margin-bottom:0.4rem;">
            Put this knowledge to work
        </div>
        <p style="color:#6B7280;font-size:0.875rem;margin-bottom:1rem;">
            Upload your resume now and see exactly where you stand.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if st.button("Analyze My Resume  ->", use_container_width=True, type="primary"):
            st.session_state.current_view = 'scorer'
            st.rerun()
