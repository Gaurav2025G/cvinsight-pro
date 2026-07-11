import streamlit as st
from frontend.services import supabase_client


def render():
    """Full-page auth screen shown before the main app."""

    # -- PAGE STYLES (auth page only, ASCII-safe) -------------------------
    st.markdown("""
<style>
/* Hide Streamlit chrome completely on auth page */
#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }
.stDeployButton { display: none !important; }

/* Hide sidebar on auth page */
section[data-testid="stSidebar"] { display: none !important; }

/* Full-page dark background */
.stApp {
    background: linear-gradient(135deg, #0B0F1A 0%, #111827 50%, #1a1060 100%) !important;
    min-height: 100vh;
}

/* Auth card */
.auth-card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    box-shadow: 0 24px 64px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.05);
    max-width: 420px;
    margin: 0 auto;
}

/* Primary button override for auth page */
.auth-card .stButton > button,
.auth-card .stFormSubmitButton > button {
    background: linear-gradient(135deg, #6366F1, #4F46E5) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1.5rem !important;
    width: 100% !important;
    box-shadow: 0 4px 16px rgba(99,102,241,0.4) !important;
    transition: all 0.2s ease !important;
}
.auth-card .stButton > button:hover,
.auth-card .stFormSubmitButton > button:hover {
    box-shadow: 0 6px 24px rgba(99,102,241,0.55) !important;
    transform: translateY(-1px) !important;
}

/* Input styling */
.auth-card input {
    border: 1.5px solid #E5E7EB !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
    transition: border-color 0.15s !important;
}
.auth-card input:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}

/* Tab styling inside auth card */
.auth-card .stTabs [data-baseweb="tab-list"] {
    background: #F3F4F6 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: none !important;
    gap: 4px !important;
}
.auth-card .stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-radius: 7px !important;
    color: #6B7280 !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    padding: 0.4rem 1rem !important;
}
.auth-card .stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #6366F1 !important;
    font-weight: 700 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1) !important;
}

/* Link button (Google) */
.auth-card [data-testid="stLinkButton"] a {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
    background: #FFFFFF !important;
    color: #374151 !important;
    border: 1.5px solid #E5E7EB !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.2s !important;
    text-decoration: none !important;
}
.auth-card [data-testid="stLinkButton"] a:hover {
    border-color: #6366F1 !important;
    background: #F5F3FF !important;
    color: #4F46E5 !important;
}
</style>
""", unsafe_allow_html=True)

    # -- BRAND HEADER (above card) ----------------------------------------
    st.markdown("""
<div style="text-align:center; padding: 2.5rem 1rem 1.5rem;">
    <div style="font-size:1.75rem; font-weight:800; color:#FFFFFF; letter-spacing:-0.02em; margin-bottom:0.3rem;">
        CV<span style="color:#818CF8;">Insight</span>
    </div>
    <div style="font-size:0.85rem; color:#64748B; font-weight:400;">
        AI-Powered Resume Intelligence
    </div>
</div>
""", unsafe_allow_html=True)

    # -- CARD WRAPPER START ------------------------------------------------
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)

    # Heading inside card
    st.markdown("""
<div style="text-align:center; margin-bottom:1.5rem;">
    <div style="font-size:1.35rem; font-weight:800; color:#111827; margin-bottom:0.3rem;">
        Welcome back
    </div>
    <div style="font-size:0.85rem; color:#6B7280;">
        Sign in to your account or create a new one
    </div>
</div>
""", unsafe_allow_html=True)

    # -- TABS: Sign in / Sign up ------------------------------------------
    tab_in, tab_up = st.tabs(["Sign in", "Create account"])

    # ---- SIGN IN --------------------------------------------------------
    with tab_in:
        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

        if st.session_state.get("auth_error"):
            st.error(st.session_state.auth_error)
            st.session_state.auth_error = None

        with st.form("signin_form", clear_on_submit=False):
            email    = st.text_input("Email address", key="signin_email",
                                     placeholder="you@example.com")
            password = st.text_input("Password", key="signin_pw",
                                     type="password", placeholder="Your password")
            submitted = st.form_submit_button("Sign in", use_container_width=True)

        if submitted:
            if not email or not password:
                st.warning("Please fill in both fields.")
            else:
                with st.spinner("Signing in..."):
                    result = supabase_client.sign_in_with_password(email, password)
                if "error" in result:
                    st.session_state.auth_error = result["error"]
                    st.rerun()
                else:
                    st.session_state.access_token  = result["access_token"]
                    st.session_state.refresh_token = result["refresh_token"]
                    st.session_state.user_id       = result["user_id"]
                    st.session_state.user_email    = result["email"]
                    st.session_state.current_view  = "landing"
                    st.rerun()

    # ---- SIGN UP --------------------------------------------------------
    with tab_up:
        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

        if st.session_state.get("auth_info"):
            st.success(st.session_state.auth_info)
            st.session_state.auth_info = None

        with st.form("signup_form", clear_on_submit=False):
            email_up    = st.text_input("Email address", key="signup_email",
                                        placeholder="you@example.com")
            password_up = st.text_input("Password", key="signup_pw",
                                        type="password", placeholder="Min 6 characters")
            submitted_up = st.form_submit_button("Create account", use_container_width=True)

        if submitted_up:
            if not email_up or not password_up:
                st.warning("Please fill in both fields.")
            elif len(password_up) < 6:
                st.warning("Password must be at least 6 characters.")
            else:
                with st.spinner("Creating your account..."):
                    result = supabase_client.sign_up_with_password(email_up, password_up)
                if "error" in result:
                    st.session_state.auth_error = result["error"]
                    st.rerun()
                elif result.get("pending_confirmation"):
                    st.session_state.auth_info = (
                        "Account created! Check your email inbox to confirm your address, "
                        "then come back and sign in."
                    )
                    st.rerun()
                else:
                    st.session_state.access_token  = result["access_token"]
                    st.session_state.refresh_token = result["refresh_token"]
                    st.session_state.user_id       = result["user_id"]
                    st.session_state.user_email    = result["email"]
                    st.session_state.current_view  = "landing"
                    st.rerun()

    # ---- DIVIDER + GOOGLE OAuth ----------------------------------------
    st.markdown("""
<div style="display:flex; align-items:center; gap:0.75rem; margin:1.25rem 0 1rem;">
    <div style="flex:1; height:1px; background:#E5E7EB;"></div>
    <div style="font-size:0.78rem; color:#9CA3AF; font-weight:500;">or continue with</div>
    <div style="flex:1; height:1px; background:#E5E7EB;"></div>
</div>
""", unsafe_allow_html=True)

    oauth = supabase_client.google_oauth_url()
    if "error" in oauth:
        st.caption(f"Google sign-in unavailable: {oauth['error']}")
    else:
        st.link_button("Continue with Google", url=oauth["url"],
                       use_container_width=True)

    # -- CARD WRAPPER END -------------------------------------------------
    st.markdown('</div>', unsafe_allow_html=True)

    # -- FOOTER -----------------------------------------------------------
    st.markdown("""
<div style="text-align:center; margin-top:2rem; padding-bottom:2rem;">
    <div style="font-size:0.75rem; color:#475569; line-height:1.7;">
        By signing in you agree to our Terms of Service and Privacy Policy.<br>
        Your data is processed securely and never sold.
    </div>
    <div style="margin-top:1rem; font-size:0.72rem; color:#334155;">
        CVInsight &mdash; AI Resume Intelligence
    </div>
</div>
""", unsafe_allow_html=True)
