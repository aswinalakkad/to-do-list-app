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
        background-color: #6b7280; /* Grey instead of black */
        color: white;
        padding: 3px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        margin-left: 8px;
    }
    .completed {
        text-decoration: line-through;
        color: #9ca3af;
    }
    </style>
""",
    unsafe_allow_html=True
)

# --- Initialize Session State ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- Add Task Form ---
with st.form("task_form", clear_on_submit=True):
    st.markdown("### ➕ Add New Task")
    title = st.text_input("Title")  # Added Label
    description = st.text_area("Description")  # Added Label
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    due_date = st.date_input("Due Date", datetime.date.today())
    submitted = st.form_submit_button("Add Task")

    if submitted and title:
        st.session_state.tasks.append({
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.datetime.now()
        })

# --- Search Bar ---
search_query = st.text_input("🔍 Search tasks", "")

# --- Filters ---
filter_option = st.radio("View", ["All", "Active", "Completed"], horizontal=True)
sort_option = st.selectbox("Sort by", ["Select All", "Priority", "Date"])

# --- Task Display ---
st.markdown("### 📋 Your Tasks")

# Apply search filter
filtered_tasks = [
    task for task in st.session_state.tasks
    if search_query.lower() in task["title"].lower() or search_query.lower() in task["description"].lower()
]

# Apply status filter
if filter_option == "Active":
    filtered_tasks = [t for t in filtered_tasks if not t["completed"]]
elif filter_option == "Completed":
    filtered_tasks = [t for t in filtered_tasks if t["completed"]]

# Apply sorting
if sort_option == "Priority":
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    filtered_tasks = sorted(filtered_tasks, key=lambda x: priority_order[x["priority"]])
elif sort_option == "Date":
    filtered_tasks = sorted(filtered_tasks, key=lambda x: x["due_date"])

# Display tasks
for idx, task in enumerate(filtered_tasks):
    st.markdown(
        f"""
        <div class="task-card">
            <div style="display:flex; align-items:center; justify-content:space-between;">
                <div>
                    <strong class="{'completed' if task['completed'] else ''}">{task['title']}</strong>
                    <span class="priority-pill">{task['priority'].upper()}</span>
                    <span style="margin-left:10px; font-size:13px; color:#6b7280;">📅 {task['due_date']}</span>
                </div>
                <div>
                    <input type="checkbox" {'checked' if task['completed'] else ''} onclick="window.location.href='?toggle={idx}'">
                </div>
            </div>
            <p class="{'completed' if task['completed'] else ''}">{task['description']}</p>
            <small style="color:#9ca3af;">Added { (datetime.datetime.now() - task['created_at']).seconds }s ago</small>
        </div>
        """,
        unsafe_allow_html=True
    )
