import streamlit as st
import requests

# PAGE CONFIG
st.set_page_config(
    page_title="✨ Autonomous QA ✨",
    page_icon="🎀",
    layout="wide"
)

st.markdown("""
<style>
    /* Import cute fonts */
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Poppins:wght@300;500&display=swap');

    /* Background Gradient */
    .stApp {
        background: linear-gradient(to bottom right, #fff0f5, #e6e6fa);
    }

    /* Titles */
    h1 {
        font-family: 'Pacifico', cursive;
        color: #ff69b4 !important;
        text-shadow: 2px 2px #fff;
    }
    h3 {
        font-family: 'Poppins', sans-serif;
        color: #ba55d3 !important;
    }

    /* GENERAL TEXT VISIBILITY */
    p, label, .stMarkdown, .stWrite, .stText, li, div {
        font-family: 'Poppins', sans-serif;
        color: #333 !important;
    }

    /* ---------------------------------------------------- */
    /* 🛠 FIX: JSON & CODE BLOCK VISIBILITY */
    /* ---------------------------------------------------- */
    
    /* Force JSON and Code blocks to have a LIGHT background */
    .stJson, .stCode, [data-testid="stJson"] {
        background-color: #ffffff !important; /* White background */
        border-radius: 10px;
        padding: 15px;
        border: 2px solid #ffb7b2;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }

    /* Force text inside JSON to be dark and readable */
    .stJson div, .stJson span, .stJson p, [data-testid="stJson"] div, [data-testid="stJson"] span {
        color: #2c3e50 !important; /* Dark Blue-Grey text */
        background-color: transparent !important;
        font-family: 'Courier New', monospace !important;
    }

    /* ---------------------------------------------------- */
    /* 🛠 FIX: MULTI-SELECT DROPDOWN VISIBILITY */
    /* ---------------------------------------------------- */
    
    /* The Clickable Input Box */
    .stMultiSelect div[data-baseweb="select"] > div {
        background-color: white !important;
        border: 2px solid #ffb7b2 !important;
        border-radius: 10px !important;
        color: #333 !important;
    }

    /* The Dropdown Menu List */
    ul[data-baseweb="menu"] {
        background-color: #fff0f5 !important;
        border: 2px solid #ffb7b2 !important;
    }

    /* The Individual Options */
    li[data-baseweb="option"] {
        color: #333 !important;
        background-color: transparent !important;
    }
    
    li[data-baseweb="option"]:hover {
        background-color: #ffb7b2 !important;
        color: white !important;
    }

    /* The "Selected" Chips */
    span[data-baseweb="tag"] {
        background-color: #ff69b4 !important;
        color: white !important;
    }

    /* ---------------------------------------------------- */

    /* BUTTON STYLING */
    .stButton>button {
        background: linear-gradient(45deg, #ff9a9e, #fad0c4);
        color: white !important;
        border-radius: 25px;
        border: none;
        font-weight: bold;
        transition: transform 0.2s;
        box-shadow: 0px 4px 10px rgba(255, 105, 180, 0.3);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(45deg, #fad0c4, #ff9a9e);
    }

    /* FILE UPLOADER FIX */
    .stFileUploader {
        background-color: rgba(255, 255, 255, 0.5);
        padding: 20px;
        border-radius: 15px;
        border: 2px dashed #ffb7b2;
    }
    [data-testid="stFileUploaderUploadedFile"] {
        color: #333 !important;
        background-color: #fff !important;
        border: 1px solid #ffd1dc;
    }
    .stFileUploader small, .stFileUploader span {
        color: #555 !important;
    }

    hr {
        border-top: 2px dashed #ffb7b2;
        margin-top: 30px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000"

# -------------------- HEADER --------------------
st.markdown("""
<h1 style="text-align:center;">
 Autonomous QA Agent 
</h1>
<p style="text-align:center; font-size:18px; color:#888;">
<i>Your testing companion! Upload docs to generate test cases & scripts. ✨</i>
</p>
""", unsafe_allow_html=True)

st.write("---")

# -------------------- STEP 1 --------------------
st.markdown("### 🌸 Step 1: Upload Documents & HTML")
st.info("✨ Please upload **checkout.html** and 3–5 support documents (requirements, API mock, UI/UX guidelines, etc.)")

uploaded_files = st.file_uploader("💖 Drop your files here:", type=["txt", "html", "pdf", "docx"], accept_multiple_files=True)

if st.button("🚀 Build Knowledge Base", use_container_width=True):
    if not uploaded_files:
        st.warning("⚠ Oopsie! Please upload files first.")
    else:
        with st.spinner("📚 Reading your files... sip some tea 🍵"):
            try:
                files = [("files", (f.name, f.getvalue(), f.type)) for f in uploaded_files]
                response = requests.post(f"{BACKEND_URL}/ingest", files=files)
                response.raise_for_status()
                st.success("🎯 Yay! Knowledge Base Built Successfully! ✨")
                st.json(response.json()["knowledge_summary"])
                st.session_state["knowledge_built"] = True
            except requests.exceptions.RequestException:
                st.error("❌ Backend not reachable. Is FastAPI running?")

st.write("---")

# -------------------- STEP 2 --------------------
st.markdown("### 🍭 Step 2: Generate Test Cases")

if st.button("📝 Generate Test Cases", use_container_width=True):
    if not st.session_state.get("knowledge_built"):
        st.warning("⚠ Honey, please build the knowledge base first!")
    else:
        with st.spinner("🧠 Brainstorming test cases... 💭"):
            response = requests.post(f"{BACKEND_URL}/generate-test-cases")

        if response.status_code == 200:
            st.success("✔ Perfect! Test cases generated successfully. 💖")
            response_json = response.json()

            # 🔍 Safely extract test cases
            test_cases_data = response_json.get("test_cases")
            if isinstance(test_cases_data, dict) and "test_cases" in test_cases_data:
                st.session_state["test_cases"] = test_cases_data["test_cases"]
            elif isinstance(test_cases_data, list):
                st.session_state["test_cases"] = test_cases_data
            else:
                st.error("🚨 Unexpected response format! Cannot extract test cases.")
                st.write("Debug →", response_json)
                st.stop()

        else:
            st.error("❌ Failed to generate test cases.")


# 🟡 Show dropdown only if valid test cases exist
if "test_cases" in st.session_state:
    test_cases = st.session_state["test_cases"]

    if not isinstance(test_cases, list) or not all(isinstance(tc, dict) for tc in test_cases):
        st.error("🚨 Test case data is invalid. Please regenerate.")
        st.write("Debug →", test_cases)

    else:
        st.markdown("#### 📌 Pick your test cases:")
        st.session_state["selected_test_ids"] = st.multiselect(
            "Select the ones you want:",
            [tc["test_id"] for tc in test_cases]  # ✔ Now safe
        )
        st.info(f"✨ Selected Test Case IDs: **{st.session_state['selected_test_ids']}**")

st.write("---")


# -------------------- STEP 3 --------------------
st.markdown("### 🦋 Step 3: Generate Selenium Scripts")

if st.button("⚙ Generate Selenium Scripts", use_container_width=True):
    if not st.session_state.get("selected_test_ids"):
        st.warning("⚠ Please select test cases first!")
    else:
        with st.spinner("🧪 Brewing your magic potion (Selenium Script)... 🪄"):
            response = requests.post(f"{BACKEND_URL}/generate-scripts", json=st.session_state["selected_test_ids"])
        if response.status_code == 200:
            script_code = response.json()["code"]
            st.success("🎉 Woohoo! Selenium Scripts Generated! 💃")
            st.code(script_code, language="python")
            st.download_button("⬇ Download Python Script 🐍", script_code, "generated_selenium_test.py", "text/x-python")
        else:
            st.error(f"❌ Error: {response.json().get('detail')}")

# -------------------- FOOTER --------------------
st.write("---")
st.markdown("""
<p style="text-align:center; color:#aaa; font-size: 14px;">
Made with 💖 & ☕ by <b>Disha Jha</b> — Autonomous QA Agent 🌸
</p>
""", unsafe_allow_html=True)
