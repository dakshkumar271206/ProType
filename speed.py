import streamlit as st
import time
import random
import os

# --- Helper Functions for External Files ---
def load_css(file_name):
    """Reads a CSS file dynamically based on the script's location."""
    # Find the exact path of the folder containing speed.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"⚠️ Could not find `{file_name}`. Please ensure it is saved in the exact same folder as `speed.py`.")

def load_html(file_name):
    """Reads an HTML file dynamically based on the script's location."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    
    try:
        with open(file_path) as f:
            st.markdown(f.read(), unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"⚠️ Could not find `{file_name}`. Please ensure it is saved in the exact same folder as `speed.py`.")
# --- Math Helper Functions ---
def calculate_errors(prompt_text, user_text):
    errors = 0
    for prompt_char, user_char in zip(prompt_text, user_text):
        if prompt_char != user_char:
            errors += 1
    errors += abs(len(prompt_text) - len(user_text))
    return errors

def calculate_wpm(start_time, end_time, user_text):
    elapsed_time_min = (end_time - start_time) / 60
    words_typed = len(user_text) / 5
    if elapsed_time_min > 0:
        return round(words_typed / elapsed_time_min, 2)
    return 0.0

# --- State Management ---
if 'test_state' not in st.session_state:
    st.session_state.test_state = "idle"
if 'target_text' not in st.session_state:
    st.session_state.target_text = ""
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0
if 'results' not in st.session_state:
    st.session_state.results = {}

# --- UI Configuration & File Loading ---
st.set_page_config(page_title="ProType | Speed Calculator", page_icon="⚡", layout="centered")

# Read and apply the external files here!
load_css("style.css")
load_html("header.html")

prompts = [
    "the quick brown fox jumps over the lazy dog",
    "pack my box with five dozen liquor jugs",
    "how vexingly quick daft zebras jump",
    "the five boxing wizards jump quickly",
    "Navigating the busy streets of New Delhi to attend a tech summit.",
    "Enjoying a crispy dosa after a long day of coding and debugging."
]

# --- Phase 1: Start Button ---
if st.session_state.test_state == "idle":
    if st.button("Initialize Typing Test", type="primary", use_container_width=True):
        st.session_state.target_text = random.choice(prompts)
        st.session_state.start_time = time.time()
        st.session_state.test_state = "active"
        st.rerun()

# --- Phase 2: The Test Interface ---
if st.session_state.test_state == "active":
    with st.container():
        st.caption("TARGET TEXT")
        st.info(st.session_state.target_text, icon="🎯")
    
    st.write("") 
    
    with st.form("typing_form", border=True):
        user_input = st.text_area("Start typing below. The timer is running!", height=120)
        
        col_space, col_btn = st.columns([3, 1])
        with col_btn:
            submitted = st.form_submit_button("Submit Run ➔", use_container_width=True)
        
        if submitted:
            end_time = time.time()
            errors = calculate_errors(st.session_state.target_text, user_input)
            wpm = calculate_wpm(st.session_state.start_time, end_time, user_input)
            
            accuracy = 0.0
            if len(st.session_state.target_text) > 0:
                accuracy_ratio = max(0, 1 - (errors / len(st.session_state.target_text)))
                accuracy = round(accuracy_ratio * 100, 2)
            
            st.session_state.results = {"wpm": wpm, "accuracy": accuracy, "errors": errors}
            st.session_state.test_state = "complete"
            st.rerun()

# --- Phase 3: Display Results ---
if st.session_state.test_state == "complete":
    st.success("Test Completed Successfully!")
    
    with st.container():
        st.markdown("### Performance Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Net Speed", f"{st.session_state.results['wpm']} WPM")
        with col2:
            st.metric("Accuracy", f"{st.session_state.results['accuracy']}%")
        with col3:
            st.metric("Error Count", st.session_state.results['errors'])
            
    st.divider()
    
    if st.button("Run Another Test", type="primary", use_container_width=True):
        st.session_state.test_state = "idle"
        st.rerun()