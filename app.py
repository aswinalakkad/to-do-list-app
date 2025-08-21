import streamlit as st
import datetime

st.set_page_config(page_title="To-Do App", page_icon="✨", layout="centered")

# --- Custom CSS for modern UI ---
st.markdown(
"""
    <style>
    .main {
        background-color: #f9fafb;
    }
    .stTextInput > div > div > input, 
    .stTextArea > div > textarea, 
    .stDateInput input {
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        padding: 10px;
    }
    .task-card {
        padding: 14px;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        margin-bottom: 10px;
        background: #ffffff;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .priority-pill {
        background-color: #374151;
        color: white;
        padding: 3px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        margin-left: 8px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- Input Fields with Labels ---
st.markdown("### Task title")
title = st.text_input("", placeholder="Enter task title")

st.markdown("### Notes (optional)")
description = st.text_area("", placeholder="Enter notes here")
