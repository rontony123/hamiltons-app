import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime
from streamlit_mic_recorder import mic_recorder

# --- PIXEL 6A MOBILE OPTIMIZATION ---
st.set_page_config(
    page_title="Hamilton's",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Mobile CSS
st.markdown("""
    <style>
    .main .block-container { padding: 1rem; }
    .stButton>button {
        width: 100%; height: 60px; border-radius: 15px;
        background-color: #4285F4; color: white; font-size: 18px;
    }
    [data-testid="stExpander"] { border-radius: 15px; background: white; }
    </style>
""", unsafe_allow_html=True)

# --- AI CONFIG ---
# PASTE YOUR KEY HERE
API_KEY = "YOUR_ACTUAL_GEMINI_KEY_HERE" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# --- DATA STORAGE ---
if 'pet_data' not in st.session_state:
    st.session_state.pet_data = {
        "Hamilton": {"breed": "Golden Retriever", "history": [], "parents": []}
    }

# --- SIDEBAR: ADD/DELETE PET ---
with st.sidebar:
    st.header("Settings")
    new_name = st.text_input("New Pet Name")
    new_breed = st.selectbox("Breed", ["Mixed", "Golden Retriever", "Bulldog", "German Shepherd", "Persian"])
    
    all_pets = list(st.session_state.pet_data.keys())
    p1 = st.selectbox("Parent 1", ["None"] + all_pets)
    
    if st.button("➕ Add Pet"):
        if new_name and new_name not in st.session_state.pet_data:
            st.session_state.pet_data[new_name] = {
                "breed": new_breed, "history": [], "parents": [p1] if p1 != "None" else []
            }
            st.rerun()
    
    st.divider()
    if st.button("🗑️ Delete Current Pet", type="secondary"):
        # Logic to delete current selection handled in main
        st.warning("Feature coming soon!")

# --- MAIN UI ---
st.title("🐾 Hamilton's")
active_pet_name = st.selectbox("Select Pet", list(st.session_state.pet_data.keys()))
pet = st.session_state.pet_data[active_pet_name]

tab1, tab2, tab3 = st.tabs(["🩺 Scan", "🌳 Family", "📜 History"])

# TAB 1: CAMERA & MIC
with tab1:
    st.subheader(f"Checking {active_pet_name}")
    photo = st.camera_input("Take health photo")
    
    st.write("Record Mood (Bark/Meow)")
    audio = mic_recorder(start_prompt="🎤 Record", stop_prompt="⏹️ Stop")

    if st.button("Analyze with AI"):
        with st.spinner("Hamilton's AI is working..."):
            # Result Simulation
            res = f"Hamilton's AI Analysis for {active_pet_name}: Everything looks normal for a {pet['breed']}!"
            st.session_state.pet_data[active_pet_name]["history"].append({
                "date": datetime.now().strftime("%d %b, %H:%M"),
                "note": res
            })
            st.success(res)

# TAB 2: FAMILY TREE (MOBILE FRIENDLY)
with tab2:
    st.subheader("Family Lineage")
    # Simple text-based tree for Android stability
    for name, data in st.session_state.pet_data.items():
        parents = data.get("parents", [])
        if parents:
            st.write(f"🐕 **{name}** is the child of **{', '.join(parents)}**")
        else:
            st.write(f"🐕 **{name}** (No parents listed)")

# TAB 3: JOURNAL
with tab3:
    st.subheader("Past Records")
    if not pet['history']:
        st.info("No records yet. Take a scan!")
    else:
        for entry in reversed(pet['history']):
            with st.expander(entry['date']):
                st.write(entry['note'])
