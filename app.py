import streamlit as st
from utils import preprocess_text
import pandas as pd



# -------Dataset load-------

df = pd.read_csv("data/faqs.csv")

st.sidebar.write(f"Total FAQs: {len(df)}")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CollegeBuddy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Top header */
    .header {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        padding: 25px 35px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.12);
    }

    .header h1 {
        margin: 0;
        font-size: 36px;
    }

    .header p {
        margin-top: 8px;
        font-size: 17px;
    }

    /* Cards */
    .card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        border: 1px solid #e5e7eb;
    }

    .card h3 {
        color: #4f46e5;
    }

    /* Chat box */
    .chat-box {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #6b7280;
        padding: 25px;
        margin-top: 40px;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
        height: 45px;
    }

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR NAVIGATION ----------------

st.sidebar.title("🎓 CollegeBuddy")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "💬 Chatbot", "ℹ️ About", "❓ Help"]
)

st.sidebar.markdown("---")
st.sidebar.caption("CollegeBuddy Chatbot")
st.sidebar.caption("PBL Project")


# ---------------- HOME PAGE ----------------

if page == "🏠 Home":

    st.markdown("""
    <div class="header">
        <h1>🎓 CollegeBuddy</h1>
        <p>Your Smart College Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
            <h3>💬 Ask Questions</h3>
            <p>Ask questions related to your college and get helpful answers.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h3>⚡ Quick Response</h3>
            <p>Get quick and simple responses from your college assistant.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <h3>🎓 Student Friendly</h3>
            <p>Designed especially to help college students.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>👋 Welcome to CollegeBuddy!</h3>
        <p>
        CollegeBuddy is a chatbot designed to help students
        find information about college-related activities,
        departments, facilities and frequently asked questions.
        </p>
        <p><b>Use the Chatbot option from the navigation menu to get started.</b></p>
    </div>
    """, unsafe_allow_html=True)


# ---------------- CHATBOT PAGE ----------------

elif page == "💬 Chatbot":

    st.markdown("""
    <div class="header">
        <h1>💬 CollegeBuddy Chatbot</h1>
        <p>Ask your college-related question</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="chat-box">', unsafe_allow_html=True)

    question = st.text_input(
        "Your Question",
        placeholder="Example: What are the college timings?"
    )

    if st.button("🚀 Ask CollegeBuddy"):

        if question.strip():

            processed = preprocess_text(question)

            st.success("Text processed successfully!")

            st.write("**Original Question:**")
            st.write(question)

            st.write("**Processed Text:**")
            st.code(processed)

            st.markdown("""
            <div class="card">
                <h3>👤 You</h3>
            </div>
            """, unsafe_allow_html=True)

            st.info(question)

            st.markdown("""
            <div class="card">
                <h3>🤖 CollegeBuddy</h3>
                <p>
                Thank you for your question! 😊<br>
                I will help you with college-related information.
                </p>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.warning("⚠️ Please enter a question first.")

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- ABOUT PAGE ----------------

elif page == "ℹ️ About":

    st.markdown("""
    <div class="header">
        <h1>ℹ️ About CollegeBuddy</h1>
        <p>Learn more about our project</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>🎓 CollegeBuddy Chatbot</h3>
        <p>
        CollegeBuddy is a college assistance chatbot developed
        as a PBL project.
        </p>

        <h3>🎯 Objective</h3>
        <p>
        The main objective is to provide students with quick
        access to useful college-related information.
        </p>

        <h3>🧠 Technologies</h3>
        <p>
        Python • Streamlit • NLP • Machine Learning
        </p>
    </div>
    """, unsafe_allow_html=True)


# ---------------- HELP PAGE ----------------

elif page == "❓ Help":

    st.markdown("""
    <div class="header">
        <h1>❓ Help</h1>
        <p>How to use CollegeBuddy</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>📌 How to use</h3>
        <ol>
            <li>Open the Chatbot page.</li>
            <li>Enter your college-related question.</li>
            <li>Click the Ask CollegeBuddy button.</li>
            <li>Read the chatbot response.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)


# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
    🎓 <b>CollegeBuddy Chatbot</b><br>
    PBL Project | AI & ML
</div>
""", unsafe_allow_html=True)