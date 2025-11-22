#version 3
import streamlit as st
import requests

# PAGE CONFIG
st.set_page_config(
    page_title="✨ Autonomous QA Bestie ✨",
    page_icon="🎀",
    layout="wide"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Poppins:wght@300;500&display=swap');
    .stApp { background: linear-gradient(to bottom right, #fff0f5, #e6e6fa); }
    h1 { font-family: 'Pacifico', cursive; color: #ff69b4 !important; text-shadow: 2px 2px #fff; }
    h3 { font-family: 'Poppins', sans-serif; color: #ba55d3 !important; }
    p, label, .stMarkdown { font-family: 'Poppins', sans-serif; color: #555; }
    .stButton>button {
        background: linear-gradient(45deg, #ff9a9e, #fad0c4);
        color: white; border-radius: 25px; border: none; font-weight: bold;
        transition: transform 0.2s; box-shadow: 0px 4px 10px rgba(255,105,180,0.3);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(45deg, #fad0c4, #ff9a9e);
    }
    .stFileUploader { background-color: rgba(255, 255, 255, 0.5); padding: 20px; border-radius: 15px; border: 2px dashed #ffb7b2; }
    .stCode { background-color: #fff !important; border-radius: 10px; border: 1px solid #ffd1dc; }
    hr { border-top: 2px dashed #ffb7b2; margin-top: 30px; margin-bottom: 30px; }
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

uploaded_files = st.file_uploader("💖 Drop your files here, darling:", type=["txt", "html", "pdf", "docx"], accept_multiple_files=True)

if st.button("🚀 Build Knowledge Base", use_container_width=True):
    if not uploaded_files:
        st.warning("⚠ Oopsie! Please upload files first, bestie.")
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
            st.session_state["test_cases"] = response.json()["test_cases"]["test_cases"]
        else:
            st.error("❌ Error generating test cases.")

if "test_cases" in st.session_state:
    st.markdown("#### 📌 Pick your test cases:")
    st.session_state["selected_test_ids"] = st.multiselect("Select the ones you want:", [tc["test_id"] for tc in st.session_state["test_cases"]])
    st.info(f"✨ Selected Test Case IDs: **{st.session_state['selected_test_ids']}**")

st.write("---")

# -------------------- STEP 3 --------------------
st.markdown("### 🦋 Step 3: Generate Selenium Scripts")

if st.button("⚙ Generate Selenium Scripts", use_container_width=True):
    if not st.session_state.get("selected_test_ids"):
        st.warning("⚠ Please select test cases first, cutie!")
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



# import streamlit as st
# import requests

# BACKEND_URL = "http://127.0.0.1:8000"

# st.set_page_config(page_title="Autonomous QA Agent", layout="wide")

# st.title("🧠 Autonomous QA Agent")
# st.write("Upload your project documents and HTML to build a testing brain and generate Selenium scripts.")

# # ------------------ Step 1: File Upload ------------------
# st.subheader("📤 Step 1: Upload Documents & HTML")

# uploaded_files = st.file_uploader(
#     "Upload 3–5 support documents + checkout.html",
#     accept_multiple_files=True
# )

# if st.button("Build Knowledge Base"):
#     if not uploaded_files:
#         st.warning("Please upload files first.")
#     else:
#         with st.spinner("Processing..."):
#             files = [("files", (f.name, f.getvalue(), f.type)) for f in uploaded_files]  # UPDATED
#             response = requests.post(f"{BACKEND_URL}/ingest", files=files)

#         if response.status_code == 200:
#             st.success("Knowledge Base Successfully Built! 🎯")
#             st.json(response.json()["knowledge_summary"])
#             st.session_state["knowledge_built"] = True
#         else:
#             st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

# # ------------------ Step 2: Generate Test Cases ------------------
# st.subheader("🧪 Step 2: Generate Test Cases")

# if st.button("Generate Test Cases"):
#     if not st.session_state.get("knowledge_built"):
#         st.warning("Please build knowledge base first.")
#     else:
#         with st.spinner("Generating using Gemini..."):
#             response = requests.post(f"{BACKEND_URL}/generate-test-cases")

#         if response.status_code == 200:
#             st.success("Test cases generated successfully! 👍")
#             test_cases = response.json()["test_cases"]["test_cases"]
#             st.session_state["test_cases"] = test_cases
#         else:
#             st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

# # Display test cases & selection
# if "test_cases" in st.session_state:
#     st.write("### Select Test Cases")
#     selected_ids = st.multiselect(
#         "Pick test cases to generate scripts for:",
#         [tc["test_id"] for tc in st.session_state["test_cases"]]
#     )
#     st.session_state["selected_test_ids"] = selected_ids

# # ------------------ Step 3: Generate Selenium Scripts ------------------
# st.subheader("🧩 Step 3: Generate Selenium Test Scripts")

# if st.button("Generate Scripts"):
#     if not st.session_state.get("selected_test_ids"):
#         st.warning("Select at least one test case first.")
#     else:
#         with st.spinner("Generating Selenium script..."):
#             response = requests.post(
#                 f"{BACKEND_URL}/generate-scripts",
#                 json=st.session_state["selected_test_ids"]
#             )

#         if response.status_code == 200:
#             st.success("Selenium scripts generated successfully! 🚀")
#             code = response.json()["code"]
#             st.code(code, language="python")

#             st.download_button(
#                 label="⬇ Download Selenium Script",
#                 data=code,
#                 file_name="generated_selenium_test.py",
#                 mime="text/x-python"
#             )
#         else:
#             st.error(f"Error: {response.json().get('detail', 'Unknown error')}")


#Version 2

# import streamlit as st
# import requests

# # -------------------- PAGE CONFIG --------------------
# st.set_page_config(
#     page_title="✨ Autonomous QA Bestie ✨",
#     page_icon="🎀",
#     layout="wide"
# )

# # -------------------- CUSTOM CSS (The Pretty Part) --------------------
# st.markdown("""
# <style>
#     /* Import a cute font */
#     @import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Poppins:wght@300;500&display=swap');

#     /* Background Gradient */
#     .stApp {
#         background: linear-gradient(to bottom right, #fff0f5, #e6e6fa);
#     }

#     /* Titles and Headers */
#     h1 {
#         font-family: 'Pacifico', cursive;
#         color: #ff69b4 !important;
#         text-shadow: 2px 2px #fff;
#     }
#     h3 {
#         font-family: 'Poppins', sans-serif;
#         color: #ba55d3 !important; /* Medium Orchid */
#     }
#     p, label, .stMarkdown {
#         font-family: 'Poppins', sans-serif;
#         color: #555;
#     }

#     /* Customizing the Buttons to be pink and rounded */
#     .stButton>button {
#         background: linear-gradient(45deg, #ff9a9e, #fad0c4);
#         color: white;
#         border-radius: 25px;
#         border: none;
#         font-weight: bold;
#         transition: transform 0.2s;
#         box-shadow: 0px 4px 10px rgba(255, 105, 180, 0.3);
#     }
#     .stButton>button:hover {
#         transform: scale(1.05);
#         color: white;
#         background: linear-gradient(45deg, #fad0c4, #ff9a9e);
#     }

#     /* Styling the File Uploader */
#     .stFileUploader {
#         background-color: rgba(255, 255, 255, 0.5);
#         padding: 20px;
#         border-radius: 15px;
#         border: 2px dashed #ffb7b2;
#     }

#     /* Code blocks background */
#     .stCode {
#         background-color: #fff !important;
#         border-radius: 10px;
#         border: 1px solid #ffd1dc;
#     }
    
#     /* Horizontal Line Styling */
#     hr {
#         border-top: 2px dashed #ffb7b2;
#         margin-top: 30px;
#         margin-bottom: 30px;
#     }
# </style>
# """, unsafe_allow_html=True)

# BACKEND_URL = "http://127.0.0.1:8000"

# # -------------------- HEADER --------------------
# st.markdown("""
# <h1 style="text-align:center;">
#  Autonomous QA Agent 
# </h1>
# <p style="text-align:center; font-size:18px; color:#888;">
# <i>Your testing companion! Upload docs to generate test cases & scripts. ✨</i>
# </p>
# """, unsafe_allow_html=True)

# st.write("---")

# # -------------------- STEP 1 --------------------
# st.markdown("### 🌸 Step 1: Upload Documents & HTML")
# st.info("✨ Please upload **checkout.html** and 3–5 support documents (requirements, API mock, UI/UX guidelines, etc.)")

# uploaded_files = st.file_uploader(
#     "💖 Drop your files here, darling:",
#     type=["txt", "html", "pdf", "docx"],
#     accept_multiple_files=True
# )

# if st.button("🚀 Build Knowledge Base", use_container_width=True):
#     if not uploaded_files:
#         st.warning("⚠ Oopsie! Please upload files first, bestie.")
#     else:
#         with st.spinner("📚 Reading your files... sip some tea 🍵"):
#             files = [("files", (f.name, f.getvalue(), f.type)) for f in uploaded_files]
#             response = requests.post(f"{BACKEND_URL}/ingest", files=files)

#         if response.status_code == 200:
#             st.success("🎯 Yay! Knowledge Base Built Successfully! ✨")
#             st.json(response.json()["knowledge_summary"])
#             st.session_state["knowledge_built"] = True
#         else:
#             st.error(f"❌ Oh no! Error: {response.json().get('detail', 'Unknown error')}")
# st.write("---")


# # -------------------- STEP 2 --------------------
# st.markdown("### 🍭 Step 2: Generate Test Cases")
# if st.button("📝 Generate Test Cases", use_container_width=True):
#     if not st.session_state.get("knowledge_built"):
#         st.warning("⚠ Honey, please build the knowledge base first!")
#     else:
#         with st.spinner("🧠 Brainstorming test cases... 💭"):
#             response = requests.post(f"{BACKEND_URL}/generate-test-cases")

#         if response.status_code == 200:
#             st.success("✔ Perfect! Test cases generated successfully. 💖")
#             test_cases = response.json()["test_cases"]["test_cases"]
#             st.session_state["test_cases"] = test_cases
#         else:
#             st.error("❌ Eek! Failed to generate test cases.")

# # Show test case selection
# if "test_cases" in st.session_state:
#     st.markdown("#### 📌 Pick your test cases:")
#     selected_ids = st.multiselect(
#         "Select the ones you want:",
#         [tc["test_id"] for tc in st.session_state["test_cases"]]
#     )
#     st.session_state["selected_test_ids"] = selected_ids
#     st.info(f"✨ Selected Test Case IDs: **{selected_ids}**")

# st.write("---")


# # -------------------- STEP 3 --------------------
# st.markdown("### 🦋 Step 3: Generate Selenium Scripts")

# if st.button("⚙ Generate Selenium Scripts", use_container_width=True):
#     if not st.session_state.get("selected_test_ids"):
#         st.warning("⚠ Please select test cases first, cutie!")
#     else:
#         with st.spinner("🧪 Brewing your magic potion (Selenium Script)... 🪄"):
#             response = requests.post(
#                 f"{BACKEND_URL}/generate-scripts",
#                 json=st.session_state["selected_test_ids"]
#             )

#         if response.status_code == 200:
#             st.success("🎉 Woohoo! Selenium Scripts Generated! 💃")
#             code = response.json()["code"]

#             st.markdown("#### 📄 Your Magic Script:")
#             st.code(code, language="python")

#             st.download_button(
#                 label="⬇ Download Python Script 🐍",
#                 data=code,
#                 file_name="generated_selenium_test.py",
#                 mime="text/x-python",
#                 use_container_width=True
#             )
#         else:
#             st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")

# # -------------------- FOOTER --------------------
# st.write("---")
# st.markdown("""
# <p style="text-align:center; color:#aaa; font-size: 14px;">
# made with 💖 and ☕ by <b>Disha Jha</b> — Autonomous QA Agent 🌸
# </p>
# """, unsafe_allow_html=True)
