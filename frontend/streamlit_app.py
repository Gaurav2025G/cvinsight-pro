import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="CVInsight — AI Resume Scorer",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── SESSION STATE ─────────────────────────────────────────────────────
for key, default in [
    ("access_token",  None),
    ("refresh_token", None),
    ("user_id",       None),
    ("user_email",    None),
    ("auth_error",    None),
    ("auth_info",     None),
    ("current_view",  "landing"),
    ("show_auth",     False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── GOOGLE OAUTH CALLBACK ─────────────────────────────────────────────
if not st.session_state.access_token and "code" in st.query_params:
    from frontend.services import supabase_client as _sc
    result = _sc.exchange_code_for_session(st.query_params["code"])
    st.query_params.clear()
    if "error" in result:
        st.session_state.auth_error = f"Google sign-in failed: {result['error']}"
    else:
        st.session_state.access_token  = result["access_token"]
        st.session_state.refresh_token = result["refresh_token"]
        st.session_state.user_id       = result["user_id"]
        st.session_state.user_email    = result["email"]
    st.rerun()

def _load_extra_css() -> str:
    try:
        p = Path(__file__).parent / "assets" / "styles.css"
        return p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""

# ── ALL CSS ───────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Syne:wght@600;700;800&display=swap');

#MainMenu, footer, header {{ visibility: hidden !important; }}
.stDeployButton {{ display: none !important; }}
.block-container {{
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
    max-width: 100% !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
}}
.stApp {{ background: #F0F4FF !important; font-family: 'Inter', sans-serif !important; }}

/* Hide streamlit sidebar completely - we don't use it */
section[data-testid="stSidebar"] {{ display: none !important; }}
button[data-testid="collapsedControl"] {{ display: none !important; }}

/* ── TOPNAV ── */
.cv-topnav {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #FFFFFF;
    border-radius: 16px;
    padding: 0.75rem 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    border: 1px solid #E5E7EB;
    position: sticky;
    top: 0.5rem;
    z-index: 100;
}}
.cv-topnav-brand {{
    font-family: 'Syne', sans-serif;
    font-size: 1.25rem;
    font-weight: 800;
    color: #111827;
    letter-spacing: -0.02em;
    display: flex;
    align-items: center;
    gap: 6px;
}}
.cv-topnav-nav {{
    display: flex;
    align-items: center;
    gap: 0.25rem;
}}
.cv-nav-link {{
    font-size: 0.875rem;
    font-weight: 500;
    color: #6B7280;
    padding: 0.4rem 0.85rem;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.15s ease;
    text-decoration: none;
    border: 1px solid transparent;
    background: transparent;
    font-family: 'Inter', sans-serif;
}}
.cv-nav-link:hover {{ color: #6366F1; background: #EEF2FF; border-color: rgba(99,102,241,0.2); }}
.cv-nav-link.active {{ color: #6366F1; background: #EEF2FF; font-weight: 600; border-color: rgba(99,102,241,0.25); }}
.cv-topnav-right {{ display: flex; align-items: center; gap: 0.75rem; }}
.cv-user-badge {{
    display: flex; align-items: center; gap: 6px;
    font-size: 0.8rem; font-weight: 600; color: #374151;
    background: #F3F4F6; border-radius: 999px;
    padding: 0.35rem 0.85rem; border: 1px solid #E5E7EB;
}}

/* ── AUTH PANEL ── */
.cv-auth-overlay {{
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.55);
    backdrop-filter: blur(4px);
    z-index: 9998;
    display: flex; align-items: center; justify-content: center;
}}
.cv-auth-panel {{
    background: #FFFFFF;
    border-radius: 20px;
    padding: 2rem 2rem 1.75rem;
    width: 100%;
    max-width: 420px;
    box-shadow: 0 24px 80px rgba(0,0,0,0.25);
    border: 1px solid #E5E7EB;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 9999;
}}
.cv-auth-title {{
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: #111827;
    margin-bottom: 0.3rem;
    letter-spacing: -0.02em;
}}
.cv-auth-sub {{
    font-size: 0.875rem;
    color: #6B7280;
    margin-bottom: 1.5rem;
}}
.cv-auth-close {{
    position: absolute; top: 1rem; right: 1rem;
    width: 32px; height: 32px;
    border-radius: 8px; border: 1px solid #E5E7EB;
    background: #F9FAFB; color: #6B7280;
    font-size: 1rem; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Inter', sans-serif; font-weight: 600;
    transition: all 0.15s ease;
}}
.cv-auth-close:hover {{ background: #FEE2E2; color: #EF4444; border-color: #FECACA; }}

/* ── MAIN BUTTONS ── */
.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, #6366F1, #4F46E5) !important;
    color: #fff !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
    font-size: 0.9rem !important; padding: 0.65rem 1.5rem !important;
    box-shadow: 0 2px 12px rgba(99,102,241,0.35) !important;
    transition: all 0.2s ease !important; font-family: 'Inter', sans-serif !important;
}}
.stButton > button[kind="primary"]:hover {{
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.5) !important;
}}
.stButton > button[kind="secondary"],
.stButton > button:not([kind]) {{
    background: #fff !important; color: #374151 !important;
    border: 1px solid #E5E7EB !important; border-radius: 10px !important;
    font-weight: 500 !important; font-size: 0.875rem !important;
    transition: all 0.18s ease !important; font-family: 'Inter', sans-serif !important;
}}
.stButton > button:not([kind]):hover {{
    border-color: #6366F1 !important; color: #6366F1 !important; background: #EEF2FF !important;
}}
.stFormSubmitButton > button {{
    background: linear-gradient(135deg, #6366F1, #4F46E5) !important;
    color: #fff !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
    font-size: 0.9rem !important; width: 100% !important;
    padding: 0.65rem 1rem !important;
    box-shadow: 0 2px 10px rgba(99,102,241,0.3) !important;
    transition: all 0.2s ease !important; font-family: 'Inter', sans-serif !important;
}}
.stFormSubmitButton > button:hover {{
    box-shadow: 0 5px 18px rgba(99,102,241,0.5) !important;
    transform: translateY(-1px) !important;
}}

/* ── INPUTS ── */
.stTextInput input, .stTextArea textarea {{
    border: 1.5px solid #E5E7EB !important; border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important; font-size: 0.9rem !important;
    background: #FAFAFA !important; color: #111827 !important;
    padding: 0.6rem 0.85rem !important;
}}
.stTextInput input:focus, .stTextArea textarea:focus {{
    border-color: #6366F1 !important; background: #fff !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}}
.stTextInput label, .stTextArea label {{
    font-size: 0.8rem !important; font-weight: 600 !important;
    color: #374151 !important; margin-bottom: 3px !important;
}}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {{
    background: #F3F4F6 !important; border-radius: 10px !important;
    padding: 4px !important; gap: 2px !important; border-bottom: none !important;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 7px !important; font-weight: 500 !important;
    font-size: 0.875rem !important; color: #6B7280 !important;
    background: transparent !important; border: none !important;
    padding: 0.4rem 1rem !important;
}}
.stTabs [aria-selected="true"] {{
    background: #fff !important; color: #6366F1 !important;
    font-weight: 700 !important; box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
}}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {{
    border: 2px dashed #D1D5DB !important; border-radius: 12px !important;
    background: #F9FAFB !important; transition: all 0.2s ease !important;
}}
[data-testid="stFileUploader"]:hover {{
    border-color: #6366F1 !important; background: #EEF2FF !important;
}}

/* ── METRICS ── */
[data-testid="metric-container"] {{
    background: #fff !important; border: 1px solid #E5E7EB !important;
    border-radius: 12px !important; padding: 1.1rem 1.35rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    font-family: 'Syne', sans-serif !important; font-weight: 800 !important;
    color: #111827 !important; font-size: 1.75rem !important;
}}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {{
    font-size: 0.72rem !important; font-weight: 600 !important;
    text-transform: uppercase !important; letter-spacing: 0.07em !important; color: #9CA3AF !important;
}}

/* ── EXPANDER ── */
[data-testid="stExpander"] {{
    border: 1px solid #E5E7EB !important; border-radius: 12px !important;
    background: #fff !important; overflow: hidden !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}}
[data-testid="stExpander"] summary {{
    font-weight: 600 !important; font-size: 0.88rem !important;
    background: #F9FAFB !important; padding: 0.8rem 1.1rem !important; color: #374151 !important;
}}

/* ── ALERT ── */
[data-testid="stAlert"] {{ border-radius: 10px !important; font-size: 0.875rem !important; }}
hr {{ border: none !important; border-top: 1px solid #E5E7EB !important; }}
[data-testid="stRadio"] label {{ font-weight: 500 !important; font-size: 0.875rem !important; }}
[data-testid="stDownloadButton"] button {{ border-radius: 10px !important; font-weight: 500 !important; }}
[data-testid="stSpinner"] {{ color: #6366F1 !important; }}
[data-testid="stLinkButton"] a {{
    background: #F9FAFB !important; color: #374151 !important;
    border: 1.5px solid #E5E7EB !important; border-radius: 10px !important;
    font-weight: 500 !important; font-size: 0.875rem !important;
    transition: all 0.15s ease !important; text-decoration: none !important;
}}
[data-testid="stLinkButton"] a:hover {{
    border-color: #6366F1 !important; color: #6366F1 !important; background: #EEF2FF !important;
}}

/* ── CUSTOM COMPONENTS ── */
.cv-hero {{
    position: relative; border-radius: 18px; padding: 3.5rem 3rem; margin-bottom: 1.5rem;
    overflow: hidden; background: linear-gradient(135deg, #0D1117 0%, #1a1060 55%, #0D1117 100%);
    box-shadow: 0 8px 40px rgba(0,0,0,0.2);
}}
.cv-hero::before {{
    content: ''; position: absolute; top: -80px; right: -60px;
    width: 320px; height: 320px; border-radius: 50%;
    background: radial-gradient(circle, rgba(99,102,241,0.45) 0%, transparent 70%); pointer-events: none;
}}
.cv-hero::after {{
    content: ''; position: absolute; bottom: -80px; left: 5%;
    width: 240px; height: 240px; border-radius: 50%;
    background: radial-gradient(circle, rgba(20,184,166,0.22) 0%, transparent 70%); pointer-events: none;
}}
.cv-hero-eyebrow {{
    display: inline-block; font-size: 0.7rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.12em; color: #818CF8;
    background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.3);
    border-radius: 999px; padding: 0.25rem 0.8rem; margin-bottom: 1rem;
}}
.cv-hero h1 {{
    font-family: 'Syne', sans-serif !important; font-size: clamp(2.2rem, 4vw, 3.2rem) !important;
    font-weight: 800 !important; color: #FFFFFF !important;
    margin: 0 0 0.75rem !important; line-height: 1.1 !important; letter-spacing: -0.03em !important;
}}
.cv-hero-sub {{ font-size: 1.05rem; color: #8B949E; line-height: 1.7; max-width: 540px; }}
.cv-hero-badge {{
    display: inline-flex; align-items: center; gap: 5px;
    font-size: 0.78rem; font-weight: 600; color: #34D399;
    background: rgba(52,211,153,0.1); border: 1px solid rgba(52,211,153,0.25);
    border-radius: 999px; padding: 0.22rem 0.7rem; margin-top: 1.2rem;
}}
.cv-feature-card {{
    background: #fff; border: 1px solid #E5E7EB; border-radius: 14px; padding: 1.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05); transition: all 0.25s ease; height: 100%;
}}
.cv-feature-card:hover {{
    box-shadow: 0 8px 28px rgba(99,102,241,0.14); transform: translateY(-4px);
    border-color: rgba(99,102,241,0.3);
}}
.cv-feature-icon {{ font-size: 1.7rem; margin-bottom: 0.7rem; display: block; }}
.cv-feature-card h3 {{
    font-size: 1rem !important; font-weight: 700 !important; color: #111827 !important;
    margin-bottom: 0.4rem !important; font-family: 'Syne', sans-serif !important;
}}
.cv-feature-card p {{ font-size: 0.875rem; color: #6B7280; line-height: 1.65; margin: 0; }}
.cv-step {{
    display: flex; gap: 1rem; align-items: flex-start; padding: 1.2rem;
    background: #fff; border: 1px solid #E5E7EB; border-radius: 12px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}}
.cv-step-number {{
    flex-shrink: 0; width: 36px; height: 36px; border-radius: 50%;
    background: linear-gradient(135deg, #6366F1, #4F46E5); color: #fff;
    font-weight: 800; font-size: 0.88rem;
    display: flex; align-items: center; justify-content: center; font-family: 'Syne', sans-serif;
}}
.cv-step-content h4 {{
    font-size: 0.92rem !important; font-weight: 700 !important;
    color: #111827 !important; margin-bottom: 0.15rem !important;
}}
.cv-step-content p {{ font-size: 0.82rem; color: #6B7280; margin: 0; }}
.cv-stat-grid {{
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 1rem; margin: 1.25rem 0;
}}
.cv-stat-item {{
    text-align: center; padding: 1.1rem;
    background: rgba(99,102,241,0.07); border: 1px solid rgba(99,102,241,0.14); border-radius: 12px;
}}
.cv-stat-item .val {{
    font-family: 'Syne', sans-serif; font-size: 1.6rem;
    font-weight: 800; color: #818CF8; display: block;
}}
.cv-stat-item .lbl {{
    font-size: 0.7rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.08em; color: #6B7280;
}}
.cv-score-card {{
    background: linear-gradient(135deg, #0D1117, #1a1060);
    border-radius: 18px; padding: 2.5rem 2rem; text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.22); position: relative; overflow: hidden;
}}
.cv-score-card::before {{
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(circle at 50% 0%, rgba(99,102,241,0.4), transparent 60%);
    pointer-events: none;
}}
.cv-score-number {{
    font-family: 'Syne', sans-serif; font-size: 5rem; font-weight: 800;
    line-height: 1; margin-bottom: 0.25rem; position: relative;
}}
.cv-score-label {{
    font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; color: #484F58; position: relative;
}}
.cv-score-interp {{ font-size: 0.9rem; color: #8B949E; position: relative; margin-top: 0.5rem; }}
.cv-score-excellent {{ color: #34D399; }}
.cv-score-good {{ color: #FBBF24; }}
.cv-score-poor {{ color: #FB7185; }}
.cv-progress-row {{ margin-bottom: 1rem; }}
.cv-progress-header {{
    display: flex; justify-content: space-between;
    align-items: center; margin-bottom: 0.35rem;
}}
.cv-progress-label {{ font-size: 0.84rem; font-weight: 600; color: #374151; }}
.cv-progress-value {{ font-size: 0.78rem; font-weight: 700; color: #6B7280; }}
.cv-progress-track {{ height: 8px; background: #F3F4F6; border-radius: 999px; overflow: hidden; }}
.cv-progress-fill {{ height: 100%; border-radius: 999px; transition: width 0.8s ease; }}
.cv-progress-fill.excellent {{ background: linear-gradient(90deg, #10B981, #34D399); }}
.cv-progress-fill.good {{ background: linear-gradient(90deg, #F59E0B, #FBBF24); }}
.cv-progress-fill.poor {{ background: linear-gradient(90deg, #EF4444, #FB7185); }}
.cv-tag {{
    display: inline-flex; align-items: center; font-size: 0.72rem;
    font-weight: 600; border-radius: 999px; padding: 0.18rem 0.6rem;
}}
.cv-tag-indigo {{ background: rgba(99,102,241,0.1); color: #4F46E5; border: 1px solid rgba(99,102,241,0.25); }}
.cv-tag-green {{ background: rgba(16,185,129,0.1); color: #059669; border: 1px solid rgba(16,185,129,0.2); }}
.cv-tag-red {{ background: rgba(244,63,94,0.1); color: #BE123C; border: 1px solid rgba(244,63,94,0.2); }}
.cv-tag-amber {{ background: rgba(245,158,11,0.1); color: #B45309; border: 1px solid rgba(245,158,11,0.2); }}
.cv-section-title {{
    font-family: 'Syne', sans-serif; font-size: 1.15rem; font-weight: 700;
    color: #111827; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.45rem;
}}
.cv-feedback-item {{
    display: flex; gap: 0.75rem; align-items: flex-start; padding: 0.75rem 1rem;
    border-radius: 9px; margin-bottom: 0.5rem; font-size: 0.875rem; line-height: 1.6;
}}
.cv-feedback-strength {{ background: rgba(16,185,129,0.07); border-left: 3px solid #10B981; color: #111827; }}
.cv-feedback-issue {{ background: rgba(239,68,68,0.07); border-left: 3px solid #EF4444; color: #111827; }}
.cv-feedback-tip {{ background: rgba(99,102,241,0.07); border-left: 3px solid #6366F1; color: #111827; }}
.cv-keyword-grid {{ display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.5rem; }}
.cv-keyword-pill {{
    display: inline-block; font-size: 0.76rem; font-weight: 600;
    background: #EEF2FF; color: #4338CA;
    border: 1px solid rgba(99,102,241,0.25); border-radius: 999px; padding: 0.2rem 0.65rem;
}}
.cv-mode-info {{
    background: #EEF2FF; border: 1px solid rgba(99,102,241,0.25);
    border-radius: 9px; padding: 0.75rem 1rem; font-size: 0.87rem; color: #4B5563; margin-bottom: 0.9rem;
}}
.cv-tip-card {{
    background: #fff; border: 1px solid #E5E7EB;
    border-radius: 12px; padding: 1.4rem; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}}
.cv-tip-list {{ list-style: none; padding: 0; margin: 0; }}
.cv-tip-list li {{
    display: flex; gap: 0.5rem; padding: 0.35rem 0;
    font-size: 0.875rem; color: #6B7280; border-bottom: 1px solid #F3F4F6;
}}
.cv-tip-list li:last-child {{ border-bottom: none; }}

{_load_extra_css()}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
#  TOP NAVIGATION BAR
# ═══════════════════════════════════════════════════════════════════════
from frontend.services import supabase_client

nav1, nav2, nav3, nav4, nav5, nav_space, nav_auth = st.columns([1, 1, 1, 1, 1, 2, 2])

with nav1:
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:800;
                color:#111827;padding:0.5rem 0;letter-spacing:-0.02em;white-space:nowrap;">
        ✦ CV<span style="color:#6366F1;">Insight</span>
    </div>
    """, unsafe_allow_html=True)

pages = [("🏠 Home", "landing"), ("🎯 Scorer", "scorer"), ("📊 History", "history"), ("📚 Resources", "resources")]
for col, (label, view) in zip([nav2, nav3, nav4, nav5], pages):
    with col:
        is_active = st.session_state.current_view == view
        btn_type = "primary" if is_active else "secondary"
        if st.button(label, key=f"topnav_{view}", use_container_width=True, type=btn_type):
            st.session_state.current_view = view
            st.rerun()

with nav_auth:
    if st.session_state.access_token:
        email = st.session_state.user_email or "User"
        short = email.split("@")[0][:12]
        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.markdown(f"""
            <div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:8px;
                        padding:0.42rem 0.75rem;font-size:0.8rem;font-weight:600;color:#166534;
                        white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                ✅ {short}
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            if st.button("Out", key="signout_top", use_container_width=True):
                supabase_client.sign_out()
                for k in ("access_token", "refresh_token", "user_id", "user_email"):
                    st.session_state[k] = None
                st.rerun()
    else:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Sign in", key="open_signin", use_container_width=True):
                st.session_state.show_auth = "signin"
                st.rerun()
        with col_b:
            if st.button("Sign up", key="open_signup", use_container_width=True, type="primary"):
                st.session_state.show_auth = "signup"
                st.rerun()

st.markdown("<div style='height:0.25rem'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
#  AUTH PANEL — inline card, shows below navbar when Sign in/up clicked
# ═══════════════════════════════════════════════════════════════════════
if st.session_state.show_auth:

    _, auth_col, _ = st.columns([1, 1.6, 1])

    with auth_col:
        # Card header
        st.markdown("""
        <div style="background:linear-gradient(135deg,#6366F1,#4F46E5);
                    border-radius:16px 16px 0 0;padding:1.5rem 2rem 1.25rem;margin-bottom:0;">
            <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;
                        color:#fff;letter-spacing:-0.02em;margin-bottom:0.25rem;">
                ✦ Welcome to CVInsight
            </div>
            <div style="font-size:0.83rem;color:rgba(255,255,255,0.72);">
                Sign in or create a free account to get started
            </div>
        </div>
        <div style="background:#fff;border:1px solid #E5E7EB;border-top:none;
                    border-radius:0 0 16px 16px;padding:1.25rem 1.5rem 0.5rem;
                    box-shadow:0 16px 48px rgba(99,102,241,0.12);margin-bottom:1rem;">
        </div>
        """, unsafe_allow_html=True)

        # Close button row
        close_col, _ = st.columns([1, 5])
        with close_col:
            if st.button("✕  Close", key="close_auth", use_container_width=True):
                st.session_state.show_auth = False
                st.rerun()

        # Error / info messages
        if st.session_state.auth_error:
            st.error(f"❌ {st.session_state.auth_error}")
            st.session_state.auth_error = None
        if st.session_state.auth_info:
            st.success(st.session_state.auth_info)
            st.session_state.auth_info = None

        # Tabs
        default_tab = 0 if st.session_state.show_auth == "signin" else 1
        tab_in, tab_up = st.tabs(["🔑  Sign in", "✨  Sign up"])

        # ── SIGN IN ──────────────────────────────────────────────────
        with tab_in:
            st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

            with st.form("signin_form", clear_on_submit=False):
                st.markdown("**Email address**")
                email_in = st.text_input("email_in_lbl", placeholder="you@example.com",
                                         key="si_email", label_visibility="collapsed")
                st.markdown("**Password**")
                pw_in = st.text_input("pw_in_lbl", placeholder="••••••••",
                                      key="si_pw", type="password", label_visibility="collapsed")
                st.markdown("<div style='height:0.25rem'></div>", unsafe_allow_html=True)
                ok_in = st.form_submit_button("Sign in →", use_container_width=True)

            if ok_in:
                if not email_in or not pw_in:
                    st.warning("Please enter both email and password.")
                else:
                    with st.spinner("Signing in…"):
                        result = supabase_client.sign_in_with_password(email_in, pw_in)
                    if "error" in result:
                        st.session_state.auth_error = result["error"]
                        st.rerun()
                    else:
                        st.session_state.access_token  = result["access_token"]
                        st.session_state.refresh_token = result["refresh_token"]
                        st.session_state.user_id       = result["user_id"]
                        st.session_state.user_email    = result["email"]
                        st.session_state.show_auth     = False
                        st.rerun()

            st.markdown("<div style='text-align:center;color:#9CA3AF;font-size:0.8rem;padding:0.5rem 0;'>— or sign in with —</div>", unsafe_allow_html=True)
            oauth = supabase_client.google_oauth_url()
            if "error" not in oauth:
                st.link_button("🔑  Continue with Google", url=oauth["url"], use_container_width=True)

        # ── SIGN UP ──────────────────────────────────────────────────
        with tab_up:
            st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

            with st.form("signup_form", clear_on_submit=False):
                st.markdown("**Email address**")
                email_up = st.text_input("email_up_lbl", placeholder="you@example.com",
                                         key="su_email", label_visibility="collapsed")
                st.markdown("**Password** *(min 6 characters)*")
                pw_up = st.text_input("pw_up_lbl", placeholder="••••••••",
                                      key="su_pw", type="password", label_visibility="collapsed")
                st.markdown("<div style='height:0.25rem'></div>", unsafe_allow_html=True)
                ok_up = st.form_submit_button("Create free account →", use_container_width=True)

            if ok_up:
                if not email_up or not pw_up:
                    st.warning("Please fill in all fields.")
                elif len(pw_up) < 6:
                    st.warning("Password must be at least 6 characters.")
                else:
                    with st.spinner("Creating account…"):
                        result = supabase_client.sign_up_with_password(email_up, pw_up)
                    if "error" in result:
                        st.session_state.auth_error = result["error"]
                        st.rerun()
                    elif result.get("pending_confirmation"):
                        st.session_state.auth_info = f"✅ Account created! Check your inbox at {result['email']} to confirm."
                        st.session_state.show_auth = False
                        st.rerun()
                    else:
                        st.session_state.access_token  = result["access_token"]
                        st.session_state.refresh_token = result["refresh_token"]
                        st.session_state.user_id       = result["user_id"]
                        st.session_state.user_email    = result["email"]
                        st.session_state.show_auth     = False
                        st.rerun()

            st.markdown("<div style='text-align:center;color:#9CA3AF;font-size:0.8rem;padding:0.5rem 0;'>— or sign up with —</div>", unsafe_allow_html=True)
            oauth = supabase_client.google_oauth_url()
            if "error" not in oauth:
                st.link_button("🔑  Continue with Google", url=oauth["url"], use_container_width=True)

        st.markdown("""
        <div style="padding:0.65rem 0.85rem;background:#F0F9FF;border:1px solid #BAE6FD;
                    border-radius:10px;font-size:0.78rem;color:#0369A1;
                    text-align:center;margin-top:0.5rem;margin-bottom:1rem;">
            🔒 Your resume is private. We never share your data.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:0 0 1.25rem 0;'>", unsafe_allow_html=True)

else:
    st.markdown("<hr style='margin:0 0 1.25rem 0;'>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
#  MAIN PAGE CONTENT
# ═══════════════════════════════════════════════════════════════════════
view = st.session_state.current_view
if view == "landing":
    from frontend.views import landing
    landing.render()
elif view == "scorer":
    from frontend.views import scorer
    scorer.render()
elif view == "history":
    from frontend.views import history
    history.render()
elif view == "resources":
    from frontend.views import resources
    resources.render()
else:
    st.session_state.current_view = "landing"
    st.rerun()