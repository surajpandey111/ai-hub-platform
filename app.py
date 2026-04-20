import streamlit as st
from streamlit_option_menu import option_menu
from auth import *
from analytics import *
from PIL import Image
from agent_llm import detect_intent_llm
import sqlite3

# Initialize database
init_db()
init_usage()

st.set_page_config(page_title="AI HUB Platform", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#020617,#0f172a);
color:white;
}

.card{
background:#111827;
padding:20px;
border-radius:15px;
text-align:center;
transition:0.3s;
}

.card:hover{
transform:scale(1.05);
box-shadow:0px 0px 20px rgba(0,255,255,0.2);
}

.title{
font-size:42px;
font-weight:700;
text-align:center;
margin-bottom:10px;
}

.subtitle{
text-align:center;
color:gray;
font-size:18px;
margin-bottom:30px;
}

</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------- LOGIN PAGE ----------
def login_page():

    st.markdown("<div class='title'>AI HUB Platform</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Login to access AI applications</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

    # ---------- LOGIN ----------
    with tab1:

        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):

            if login_user(user, pwd):

                st.session_state.logged_in = True
                st.session_state.username = user

                st.success("Login successful")
                st.rerun()

            else:
                st.error("Invalid username or password")

    # ---------- REGISTER ----------
    with tab2:

        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Create Account"):

            if create_user(new_user, new_pass):
                st.success("Account created successfully. Please login.")

            else:
                st.error("User already exists")


def dashboard():

    with st.sidebar:

        st.write(f"👤 Logged in as: **{st.session_state.username}**")

        selected = option_menu(
            "AI HUB",
            ["Home", "Analytics", "Logout"],
            icons=["house", "bar-chart", "box-arrow-right"],
            menu_icon="robot"
        )

    # ---------- LOGOUT ----------
    if selected == "Logout":

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.rerun()

    # ---------- HOME ----------
    if selected == "Home":

        st.markdown("<div class='title'>AI Applications</div>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle'>Choose or Ask AI</div>", unsafe_allow_html=True)

        # 🤖 AGENT INPUT
        st.markdown("## 🤖 Smart AI Assistant (Auto Mode)")

        user_query = st.text_input("💬 Ask anything (PDF / Cooking / College Info)")

        if user_query:

            with st.spinner("🤖 Thinking..."):

                intent = detect_intent_llm(user_query)

            if intent == "PDF":
                st.success("📄 AI Selected: PDF → Excel System")
                log_usage(st.session_state.username, "PDF→Excel")
                st.markdown("[🚀 Launch PDF AI](https://gyanmaipdf-to-excel-super-smart.streamlit.app/)")

            elif intent == "COOKING":
                st.success("🍳 AI Selected: Cooking Assistant")
                log_usage(st.session_state.username, "Cooking AI")
                st.markdown("[🚀 Launch Cooking AI](https://smart-cook-ai.streamlit.app/)")

            elif intent == "CHATBOT":
                st.success("🎓 AI Selected: REC Chatbot")
                log_usage(st.session_state.username, "REC Bot")
                st.markdown("[🚀 Launch Chatbot](https://rec-azamgarh-chatbot.streamlit.app/)")

            else:
                st.warning("❓ Could not understand. Try again.")

        st.markdown("---")

        # 🔁 MANUAL MODE
        col1, col2, col3 = st.columns(3)

        with col1:
            st.image("assets/research_pdf.png")
            if st.button("Open PDF → Excel AI"):
                log_usage(st.session_state.username, "PDF→Excel")
                st.markdown("[🚀 Launch Application](https://gyanmaipdf-to-excel-super-smart.streamlit.app/)")

        with col2:
            st.image("assets/cooking.png")
            if st.button("Open Cooking AI"):
                log_usage(st.session_state.username, "Cooking AI")
                st.markdown("[🚀 Launch Application](https://smart-cook-ai.streamlit.app/)")

        with col3:
            st.image("assets/rec_azamgarh.png")
            if st.button("Open REC Azamgarh Bot"):
                log_usage(st.session_state.username, "REC Bot")
                st.markdown("[🚀 Launch Application](https://rec-azamgarh-chatbot.streamlit.app/)")

    # ---------- ANALYTICS ----------
    if selected == "Analytics":

        st.title("📊 Platform Analytics")

        conn = sqlite3.connect("users.db")
        data = conn.execute("SELECT * FROM usage").fetchall()

        if data:
            st.table(data)
        else:
            st.info("No usage data yet.")

  


# ---------- RUN APP ----------
if not st.session_state.logged_in:

    login_page()

else:

    dashboard()