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
        background-color: #6b7280; /* changed to grey */
        color: white;
        padding: 3px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        margin-left: 8px;
    }
    .completed {
        text-decoration: line-through;
        text-decoration-thickness: 2px;
        text-decoration-color: #9ca3af;
    }
    </style>
""",
    unsafe_allow_html=True
)

# --- Session State for tasks ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- Search Option ---
search_query = st.text_input("🔍 Search tasks")

# --- Task Input Form ---
st.subheader("➕ Add New Task")

title = st.text_input("Task Title ✏️", key="title_input")
description = st.text_area("Task Description 📝", key="desc_input")
priority = st.selectbox("Priority 🚩", ["LOW", "MEDIUM", "HIGH"])
due_date = st.date_input("Due Date 📅", datetime.date.today())

if st.button("Add Task"):
    if title.strip():
        st.session_state.tasks.append({
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "completed": False,
            "added": datetime.datetime.now()
        })
        st.success("Task added successfully ✅")
    else:
        st.warning("⚠️ Please enter a title for the task")

# --- Task List ---
st.subheader("📋 Your Tasks")

for i, task in enumerate(st.session_state.tasks):
    # --- Apply search filter ---
    if search_query.lower() not in task["title"].lower() and search_query.lower() not in task["description"].lower():
        continue

    completed_class = "completed" if task["completed"] else ""
    with st.container():
        st.markdown(
            f"""
            <div class="task-card">
                <strong class="{completed_class}">{task['title']}</strong>
                <span class="priority-pill">{task['priority']}</span> 
                <span>📅 {task['due_date']}</span>
                <p class="{completed_class}">{task['description']}</p>
                <small>Added { (datetime.datetime.now() - task['added']).seconds }s ago</small>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        col1, col2 = st.columns([0.2, 0.8])
        with col1:
            if st.checkbox("Done", value=task["completed"], key=f"check_{i}"):
                st.session_state.tasks[i]["completed"] = True
        with col2:
            if st.button("❌ Delete", key=f"delete_{i}"):
                st.session_state.tasks.pop(i)
                st.experimental_rerun()
