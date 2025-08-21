import streamlit as st
import datetime
from datetime import datetime as dt

# Initialize session state for tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Function to add a task
def add_task(title, description, priority, due_date):
    st.session_state.tasks.append({
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "completed": False,
        "created_at": dt.now()
    })

# Function to delete a task
def delete_task(index):
    st.session_state.tasks.pop(index)

# Function to toggle completion
def toggle_complete(index):
    st.session_state.tasks[index]["completed"] = not st.session_state.tasks[index]["completed"]

# Sidebar for adding tasks
st.sidebar.header("Add New Task")

title = st.sidebar.text_input("Task Title ✍️")   # Added label
description = st.sidebar.text_area("Task Description 📝")  # Added label
priority = st.sidebar.selectbox("Priority 🚦", ["Low", "Medium", "High"])
due_date = st.sidebar.date_input("Due Date 📅", min_value=dt.today())

if st.sidebar.button("Add Task"):
    if title.strip():
        add_task(title, description, priority, due_date)
        st.sidebar.success("✅ Task added!")
    else:
        st.sidebar.error("⚠️ Title cannot be empty.")

# Filters
st.sidebar.header("Filters & Sort")
status_filter = st.sidebar.selectbox("Show Tasks", ["All", "Active", "Completed"])
priority_filter = st.sidebar.selectbox("Filter by Priority", ["All", "Low", "Medium", "High"])
sort_option = st.sidebar.selectbox("Sort by", ["Date Added", "Due Date", "Priority"])

# Apply filters
tasks = st.session_state.tasks

if status_filter == "Active":
    tasks = [t for t in tasks if not t["completed"]]
elif status_filter == "Completed":
    tasks = [t for t in tasks if t["completed"]]

if priority_filter != "All":
    tasks = [t for t in tasks if t["priority"] == priority_filter]

# Sorting
if sort_option == "Due Date":
    tasks = sorted(tasks, key=lambda x: x["due_date"])
elif sort_option == "Priority":
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    tasks = sorted(tasks, key=lambda x: priority_order[x["priority"]])
else:
    tasks = sorted(tasks, key=lambda x: x["created_at"])

# Display tasks
st.header("📝 Task List")

for i, task in enumerate(tasks):
    with st.container():
        col1, col2, col3, col4 = st.columns([0.1, 4, 0.7, 0.5])
        
        # Checkbox to mark complete
        if col1.checkbox("", value=task["completed"], key=f"complete_{i}"):
            toggle_complete(i)
        
        # Task details
        with col2:
            title_style = "text-decoration: line-through; color: grey;" if task["completed"] else "font-weight: bold;"
            st.markdown(
                f"<div style='{title_style}'>{task['title']}</div>", unsafe_allow_html=True
            )
            st.write(task["description"])
            st.caption(f"Added {task['created_at'].strftime('%b %d, %Y %I:%M %p')}")
        
        # Priority badge
        col3.markdown(
            f"<span style='background-color:#d3d3d3; color:white; padding:4px 8px; border-radius:8px; font-size:12px; font-weight:bold;'>{task['priority'].upper()}</span>",
            unsafe_allow_html=True
        )
        
        # Due date
        col3.write(task["due_date"])
        
        # Action buttons
        with col4:
            if st.button("🖊️", key=f"edit_{i}"):
                st.info("Edit feature coming soon...")
            if st.button("🗑️", key=f"delete_{i}"):
                delete_task(i)
                st.rerun()
