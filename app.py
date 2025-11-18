import streamlit as st

# Import your 3 main modules
from fitness_gui import fitness_dashboard
from disease_recognition import disease_recognition_page
from voice_assistant import ai_assistant_page


# ----------------------------
# PAGE SETTINGS
# ----------------------------
st.set_page_config(
    page_title="ZENIVA - AI Health System",
    layout="centered",
    page_icon="🧠"
)

# ----------------------------
# HOME PAGE UI
# ----------------------------
st.title("🧠 ZENIVA – AI Health System")
st.write("Select a module to continue:")

module = st.selectbox(
    "Choose Module:",
    [
        "🏃 Fitness Tracking",
        "🩺 Disease Recognition",
        "🤖 AI Assistant"
    ]
)

# ----------------------------
# LOAD SELECTED MODULE
# ----------------------------
if module == "🏃 Fitness Tracking":
    fitness_dashboard()

elif module == "🩺 Disease Recognition":
    disease_recognition_page()

elif module == "🤖 AI Assistant":
    ai_assistant_page()
