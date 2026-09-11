
import streamlit as st
import pandas as pd
from pathlib import Path
from textwrap import dedent
from utils import preprocess_text

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="CollegeBuddy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PATHS / DATA
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "assets"

try:
    df = pd.read_csv(BASE_DIR / "data" / "faq.csv")
except Exception:
    df = pd.DataFrame()

# ============================================================
# SESSION STATE
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "page" not in st.session_state:
    st.session_state.page = "Home"

# ============================================================
# HELPERS
# ============================================================
def asset(name: str) -> str:
    return str(ASSET_DIR / name)

def go_to(page: str):
    st.session_state.page = page
    st.rerun()

def clear_chat():
    st.session_state.messages = []
    st.rerun()

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root{
    --navy:#101c52;
    --text:#17234f;
    --muted:#5f6d92;
    --purple:#5a45e8;
    --purple2:#6c5ce9;
    --lavender:#eeefff;
    --line:#dfe3f2;
    --page:#f8f9fe;
    --white:#ffffff;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 90% 0%, rgba(111,95,235,.07), transparent 25%),
        linear-gradient(180deg, #fbfcff 0%, #f7f8fd 100%);
    color: var(--text);
}

.block-container {
    padding: 0 !important;
    max-width: none !important;
}

/* Hide Streamlit chrome */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
[data-testid="stToolbar"] {display:none !important;}

/* ---------------- TOP BAR ---------------- */
.topbar {
    height: 86px;
    background: rgba(255,255,255,.96);
    border-bottom: 1px solid #e5e8f2;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding: 0 28px 0 30px;
    position: sticky;
    top:0;
    z-index:50;
}

.brand-img {
    width: 248px;
    height:auto;
    object-fit:contain;
}

.chatbot-img {
    width: 170px !important;
    height: 60px !important;
    object-fit: contain !important;
    display: block !important;
    flex-shrink: 0 !important;
}

/* ---------------- SIDEBAR ---------------- */
section[data-testid="stSidebar"] {
    width: 315px !important;
    min-width: 315px !important;
    background: #f8f9fe !important;
    border-right: 1px solid #e2e6f1;
}

section[data-testid="stSidebar"] > div {
    padding: 0 !important;
}

section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.25rem;
}

.sidebar-inner {
    padding: 22px 22px 0 22px;
}

.side-logo {
    width: 245px;
    margin: 0 0 30px 5px;
}

.side-nav-label {
    display:none;
}

section[data-testid="stSidebar"] .stButton > button {
    width:100% !important;
    height:52px !important;
    border:0 !important;
    border-radius:14px !important;
    background:transparent !important;
    color:#14204d !important;
    text-align:left !important;
    padding:0 20px !important;
    font-size:17px !important;
    font-weight:500 !important;
    box-shadow:none !important;
    margin: 2px 0 !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background:#f0efff !important;
    color:#4938d2 !important;
}

section[data-testid="stSidebar"] .active-nav > button,
section[data-testid="stSidebar"] .active-nav button {
    background:linear-gradient(90deg,#ecebff,#e3e2ff) !important;
    color:#4b3bd5 !important;
    font-weight:600 !important;
}

.sidebar-stat {
    margin: 38px 2px 18px;
    padding: 18px 20px;
    border-radius:18px;
    background:linear-gradient(135deg,#f0f2ff,#e9ecff);
    border:1px solid #e4e7f6;
}
.sidebar-stat .title {
    font-size:16px;
    font-weight:600;
    color:#17235a;
}
.sidebar-stat .number {
    font-size:34px;
    font-weight:800;
    color:#4436d2;
    line-height:1.15;
    margin-top:7px;
}
.sidebar-stat .sub {
    color:#68749a;
    font-size:14px;
    margin-top:3px;
}

.quote-card {
    margin: 20px 2px 0;
    padding: 25px 18px;
    border-radius:18px;
    background:linear-gradient(145deg,#f0f2ff,#f8f9ff);
    border:1px solid #e5e8f5;
    text-align:center;
}
.quote-card .quote {
    color:#5762a1;
    font-family:Georgia,serif;
    font-style:italic;
    font-size:23px;
    line-height:1.35;
}
.quote-card .by {
    color:#68749b;
    font-size:14px;
    margin-top:15px;
}

.campus-img {
    width:100%;
    margin-top: 35px;
    opacity:.88;
}

/* ---------------- MAIN ---------------- */
.main-wrap {
    padding: 24px 28px 10px 28px;
}

.hero {
    min-height: 312px;
    border-radius: 16px;
    background: linear-gradient(105deg,#eef0ff 0%,#e8eaff 53%,#dde4ff 100%);
    border:1px solid #dce1f3;
    overflow:hidden;
    position:relative;
    display:flex;
    align-items:stretch;
}

.hero-copy {
    width:58%;
    padding:40px 0 30px 30px;
    position:relative;
    z-index:2;
}
.hero-kicker {
    letter-spacing:7px;
    font-size:17px;
    color:#243367;
    font-weight:600;
    margin-bottom:10px;
}
.hero h1 {
    font-size:54px;
    line-height:1.03;
    letter-spacing:-2px;
    margin:0;
    color:#0d1749;
    font-weight:800;
}
.hero-sub {
    margin-top:15px;
    font-size:19px;
    color:#26365e;
}
.hero-art {
    position:absolute;
    right:0;
    top:0;
    width:42%;
    height:100%;
    object-fit:cover;
    object-position:left center;
}

.feature-row {
    display:flex;
    gap:48px;
    margin-top:35px;
}
.feature {
    display:flex;
    gap:14px;
    align-items:flex-start;
}
.feature-icon {
    width:43px;
    height:43px;
    border-radius:12px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:#e8e9ff;
    color:#5545df;
    font-size:24px;
    flex:none;
}
.feature-title {
    color:#162251;
    font-weight:700;
    font-size:16px;
}
.feature-sub {
    color:#667298;
    font-size:13px;
    margin-top:3px;
}

.section-title {
    font-size:27px;
    font-weight:800;
    color:#101d4e;
    margin:25px 0 13px;
}

.card {
    background:#fff;
    border:1px solid #dde2ef;
    border-radius:16px;
    box-shadow:0 4px 18px rgba(31,44,90,.035);
}

.start-card {
    min-height:245px;
    padding:28px 30px;
    display:flex;
    align-items:center;
    gap:27px;
}
.start-icon {
    width:115px;
    height:115px;
    border-radius:50%;
    background:#f1f2ff;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:56px;
    flex:none;
}
.start-title {
    font-size:26px;
    font-weight:800;
    color:#101d4e;
}
.start-text {
    font-size:17px;
    line-height:1.5;
    color:#667298;
    margin:7px 0 20px;
}
.primary-btn {
    background:linear-gradient(90deg,#5640df,#654eea);
    color:white;
    border-radius:28px;
    padding:11px 29px;
    font-size:18px;
    font-weight:600;
    display:inline-block;
}

.ask-card {
    min-height:245px;
    padding:22px;
}
.ask-title {
    font-size:19px;
    font-weight:800;
    color:#152150;
    margin-bottom:13px;
}
.example {
    background:#f4f5fb;
    border-radius:11px;
    padding:7px 12px;
    margin:7px 0;
    color:#334063;
    font-size:14px;
}

.about-card {
    margin-top:18px;
    padding:25px 30px;
    display:flex;
    gap:25px;
    align-items:flex-start;
}
.about-icon {
    width:72px;
    height:72px;
    border-radius:50%;
    background:#f2f3ff;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:38px;
    flex:none;
}
.about-title {
    font-size:20px;
    font-weight:800;
    color:#152150;
    margin-bottom:10px;
}
.about-text {
    color:#657095;
    font-size:16px;
    line-height:1.6;
}

.footer-row {
    display:flex;
    justify-content:space-between;
    padding:30px 4px 15px;
    color:#647091;
    font-size:14px;
}

/* ---------------- CHAT PAGE ---------------- */
.chat-shell {
    background:#fff;
    border:1px solid #e0e4f0;
    border-radius:17px;
    box-shadow:0 5px 25px rgba(32,47,93,.045);
    overflow:hidden;
}

.chat-header {
    min-height:104px;
    padding:18px 26px;
    border-bottom:1px solid #e5e8f1;
    display:flex;
    align-items:center;
    justify-content:space-between;
}
.chat-header-left {
    display:flex;
    align-items:center;
    gap:18px;
}
.chat-bubble-icon {
    width:54px;
    height:54px;
    border-radius:50%;
    background:#eef0ff;
    display:flex;
    align-items:center;
    justify-content:center;
    color:#4e40df;
    font-size:30px;
}
.chat-title {
    font-size:29px;
    font-weight:800;
    color:#101d4e;
}
.chat-sub {
    color:#697497;
    font-size:16px;
}
.powered {
    background:#f1f2ff;
    border-radius:14px;
    padding:12px 18px;
    color:#1e2a54;
    font-size:13px;
}
.chat-body {
    height:520px;
    overflow-y:auto;
    padding:20px 24px;
    background:#fff;
}
.msg-row {
    display:flex;
    margin:0 0 24px;
    gap:12px;
}
.msg-row.user {
    justify-content:flex-end;
}
.avatar {
    width:43px;
    height:43px;
    border-radius:50%;
    background:#eef1ff;
    display:flex;
    align-items:center;
    justify-content:center;
    flex:none;
    font-size:22px;
}
.msg {
    max-width: 72%;
    border-radius: 15px;
    padding: 12px 16px;
    color: #202b50;
    line-height: 1.5;
    font-size: 15px;
}
.msg.bot {
    background:#f0f1f7;
}
.msg.user {
    background: linear-gradient(135deg,#6858ea,#5c49dd);
    color:#fff;
    border-bottom-right-radius:5px;

    /* Keep short user messages on one line */
    width: fit-content;
    max-width: 100%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.time {
    font-size:11px;
    color:#8a92a8;
    margin-top:5px;
}
.time.right { text-align:right; }

.chat-input-wrap {
    border-top:1px solid #e5e8f1;
    padding:15px 22px 16px;
    background:#fff;
}

/* Streamlit inputs */
.stTextInput input, .stTextArea textarea {
    border:1px solid #d8deee !important;
    border-radius:13px !important;
    color:#1a2550 !important;
    background:#fff !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color:#8790a9 !important;
}
.stButton > button {
    border:0 !important;
    border-radius:12px !important;
    font-weight:600 !important;
}
.primary-streamlit > button {
    background:linear-gradient(90deg,#5540df,#654ce9) !important;
    color:#fff !important;
}
.secondary-streamlit > button {
    background:#f1f2ff !important;
    color:#4a3ad0 !important;
    border:1px solid #e0e2f5 !important;
}

/* Keep default widget labels compact */
.stTextInput label, .stTextArea label {
    display:none !important;
}

/* Responsive */
@media (max-width: 1000px) {
    section[data-testid="stSidebar"] { width:245px !important; min-width:245px !important; }
    .hero h1 {font-size:42px;}
    .feature-row {gap:20px;}
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# TOP BAR
# ============================================================
st.markdown(
    f"""
<div class="topbar">
    <img class="brand-img" src="data:image/png;base64,{__import__('base64').b64encode(open(asset('collegebuddy_logo.png'),'rb').read()).decode()}">
    <img class="chatbot-img" src="data:image/png;base64,{__import__('base64').b64encode(open(asset('chatbot-chat-message-vectorart_78370-4104.avif'),'rb').read()).decode()}">
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown('<div class="sidebar-inner">', unsafe_allow_html=True)

    st.markdown(
        f'<img class="side-logo" src="data:image/png;base64,{__import__("base64").b64encode(open(asset("collegebuddy_logo.png"),"rb").read()).decode()}">',
        unsafe_allow_html=True,
    )

    nav_items = [
        ("Home", "⌂"),
        ("Chatbot", "💬"),
        ("About", "ⓘ"),
    ]

    for label, icon in nav_items:
        active = st.session_state.page == label
        st.markdown(
            '<div class="active-nav">' if active else '<div>',
            unsafe_allow_html=True,
        )
        if st.button(f"{icon}    {label}", key=f"nav_{label}", use_container_width=True):
            go_to(label)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="sidebar-stat">
            <div class="title">▣ &nbsp; FAQ Dataset</div>
            <div class="number">{len(df)}</div>
            <div class="sub">Verified FAQs</div>
        </div>
        <div class="quote-card">
            <div class="quote">“Ask. Learn.<br>Grow.”</div>
            <div class="by">— CollegeBuddy</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    campus_b64 = __import__("base64").b64encode(open(asset("sidebar_campus.png"), "rb").read()).decode()
    st.markdown(
        f'<img class="campus-img" src="data:image/png;base64,{campus_b64}">',
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# HOME
# ============================================================
if st.session_state.page == "Home":
    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    hero_b64 = __import__("base64").b64encode(open(asset("hero_art.png"), "rb").read()).decode()

    # IMPORTANT: dedent removes Python indentation from the HTML.
    # Without this, some Streamlit/Markdown versions can display the
    # HTML block as raw code instead of rendering the Home UI.
    hero_html = dedent(f"""
    <div class="hero">
        <div class="hero-copy">
            <div class="hero-kicker">WELCOME TO</div>
            <h1>CollegeBuddy</h1>
            <div class="hero-sub">Your AI-powered assistant for all college-related queries.</div>
            <div class="feature-row">
                <div class="feature">
                    <div class="feature-icon">✓</div>
                    <div>
                        <div class="feature-title">Reliable Information</div>
                        <div class="feature-sub">From official sources</div>
                    </div>
                </div>
                <div class="feature">
                    <div class="feature-icon">ϟ</div>
                    <div>
                        <div class="feature-title">Quick Answers</div>
                        <div class="feature-sub">Using NLP + TF-IDF</div>
                    </div>
                </div>
                <div class="feature">
                    <div class="feature-icon">♧</div>
                    <div>
                        <div class="feature-title">AI Support</div>
                        <div class="feature-sub">Powered by Gemini<br>(for unmatched queries)</div>
                    </div>
                </div>
            </div>
        </div>
        <img class="hero-art" src="data:image/png;base64,{hero_b64}" alt="CollegeBuddy illustration">
    </div>
    <div class="section-title">Get Started</div>
    """)

    st.markdown(hero_html, unsafe_allow_html=True)

    c1, c2 = st.columns([2.05, 1], gap="small")

    with c1:
        st.markdown(
            """
            <div class="card start-card">
                <div class="start-icon">💬</div>
                <div>
                    <div class="start-title">Have a question?</div>
                    <div class="start-text">
                        Ask anything related to admissions, fees, exams, departments,
                        placements, hostel facilities and more.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Chatbot  →", key="open_chat", use_container_width=False):
            go_to("Chatbot")

    with c2:
        st.markdown(
            """
            <div class="card ask-card">
                <div class="ask-title">What can you ask?</div>
                <div class="example">“What is the B.Tech fee structure?”</div>
                <div class="example">“Are hostel facilities available?”</div>
                <div class="example">“How can I apply for admission?”</div>
                <div class="example">“What scholarships are offered?”</div>
                <div class="example">“What are the placement statistics?”</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="card about-card">
            <div class="about-icon">💡</div>
            <div>
                <div class="about-title">About CollegeBuddy</div>
                <div class="about-text">
                    CollegeBuddy is an AI-powered chatbot designed to help ITM University
                    Gwalior students get quick and accurate information. It uses NLP with
                    TF-IDF and Cosine Similarity to retrieve answers from an official FAQ
                    dataset, and Gemini AI as a fallback for unmatched queries.
                </div>
            </div>
        </div>

        <div class="footer-row">
            <div>© 2025 CollegeBuddy &nbsp;|&nbsp; ITM University Gwalior</div>
            <div>Built with ❤️ for Students</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# CHATBOT
# ============================================================
elif st.session_state.page == "Chatbot":
    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="chat-shell">
            <div class="chat-header">
                <div class="chat-header-left">
                    <div class="chat-bubble-icon">💬</div>
                    <div>
                        <div class="chat-title">Chat with CollegeBuddy</div>
                        <div class="chat-sub">Ask your college-related questions and get instant answers.</div>
                    </div>
                </div>
                <div class="powered">⚡ &nbsp; Powered by NLP + TF-IDF<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;with Gemini AI (fallback)</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Chat history
    st.markdown('<div class="chat-shell" style="margin-top:0;border-top:0;border-radius:0 0 17px 17px;">', unsafe_allow_html=True)
    st.markdown('<div class="chat-body">', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown(
            """
            <div class="msg-row">
                <div class="avatar">🤖</div>
                <div>
                    <div class="msg bot">
                        Hi! 👋<br>
                        I’m CollegeBuddy, your AI assistant for ITM University Gwalior.<br>
                        You can ask me about admissions, fees, exams, departments,
                        placements, hostel facilities and more.
                    </div>
                    <div class="time">11:24 AM</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        safe_content = str(content).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")

        if role == "user":
            st.markdown(
                f"""
                <div class="msg-row user">
                    <div>
                        <div class="msg user">{safe_content}</div>
                        <div class="time right">Now</div>
                    </div>
                    <div class="avatar">👤</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="msg-row">
                    <div class="avatar">🤖</div>
                    <div>
                        <div class="msg bot">{safe_content}</div>
                        <div class="time">Now</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Controls
    st.markdown('<div class="chat-input-wrap">', unsafe_allow_html=True)
    input_col, send_col, clear_col = st.columns([8, 1.1, 1.1], gap="small")

    with input_col:
        question = st.text_input(
            "Question",
            placeholder="Type your question here...",
            key="question_box",
        )

    with send_col:
        st.markdown('<div class="primary-streamlit">', unsafe_allow_html=True)
        send = st.button("➤", key="send_question", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with clear_col:
        st.markdown('<div class="secondary-streamlit">', unsafe_allow_html=True)
        clear = st.button("Clear", key="clear_chat_btn", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div style="color:#8790a9;font-size:12px;margin-top:6px;">Press Enter to send &nbsp;|&nbsp; Ask clear and specific questions for better results.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Submit
    if send and question.strip():
        question = question.strip()
        st.session_state.messages.append({"role": "user", "content": question})

        try:
            processed_question = preprocess_text(question)
        except Exception:
            processed_question = question

        # Keep your existing answer logic here.
        # This UI version does not change utils.py.
        answer = (
            "Thank you for your question! 😊\n\n"
            "I will help you with college-related information."
        )

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

    if clear:
        clear_chat()

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# ABOUT
# ============================================================
elif st.session_state.page == "About":
    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-title" style="margin-top:10px;">About CollegeBuddy</div>
        <div class="card about-card" style="margin-top:0;">
            <div class="about-icon">💡</div>
            <div>
                <div class="about-title">CollegeBuddy</div>
                <div class="about-text">
                    CollegeBuddy is a college assistance chatbot developed as a PBL project.
                    The interface is designed to give students a clean and simple place to
                    find college-related information.
                </div>
            </div>
        </div>

        <div class="section-title">Objective</div>
        <div class="card" style="padding:25px 30px;">
            <div class="about-text">
                The main objective is to provide students with quick access to useful
                college-related information.
            </div>
        </div>

        <div class="section-title">Technologies</div>
        <div class="card" style="padding:25px 30px;">
            <div class="about-text">Python • Streamlit • NLP • Machine Learning</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)