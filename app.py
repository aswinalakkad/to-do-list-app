import streamlit as st
from datetime import datetime

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

st.title("✅ To-Do App")

# --- Add Task Form ---
with st.form("add_task"):
    title = st.text_input("Task Title")
    notes = st.text_area("Notes (optional)")
    due = st.date_input("Due Date")
    priority = st.selectbox("Priority", ["Select", "Low", "Medium", "High"])
    submitted = st.form_submit_button("Add Task")

    if submitted:
        if title and priority != "Select":
            st.session_state.tasks.append(
                {
                    "title": title,
                    "notes": notes,
                    "due": due,
                    "priority": priority,
                    "completed": False,
                    "created_at": datetime.now(),
                }
            )
            st.success("Task added successfully ✅")
        else:
            st.warning("Please enter a title and select a priority")

# --- Filters & Sorting ---
st.sidebar.header("🔎 Filter & Sort")
status_filter = st.sidebar.radio("Show", ["All", "Active", "Completed"])
priority_filter = st.sidebar.selectbox(
    "Filter by Priority", ["All", "Low", "Medium", "High"]
)
sort_option = st.sidebar.selectbox("Sort by", ["Created Time", "Due Date", "Priority"])

# --- Apply Filters ---
filtered_tasks = st.session_state.tasks
if status_filter == "Active":
    filtered_tasks = [t for t in filtered_tasks if not t["completed"]]
elif status_filter == "Completed":
    filtered_tasks = [t for t in filtered_tasks if t["completed"]]

if priority_filter != "All":
    filtered_tasks = [t for t in filtered_tasks if t["priority"] == priority_filter]

# --- Apply Sorting ---
if sort_option == "Created Time":
    filtered_tasks = sorted(filtered_tasks, key=lambda x: x["created_at"], reverse=True)
elif sort_option == "Due Date":
    filtered_tasks = sorted(filtered_tasks, key=lambda x: x["due"])
elif sort_option == "Priority":
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    filtered_tasks = sorted(filtered_tasks, key=lambda x: priority_order[x["priority"]])

# --- Task List Display ---
st.subheader("📋 Your Tasks")

if not filtered_tasks:
    st.info("No tasks found.")
else:
    for i, task in enumerate(filtered_tasks):
        with st.container():
            col1, col2, col3 = st.columns([0.1, 4, 0.5])

            # Checkbox for complete
            with col1:
                done = st.checkbox("", value=task["completed"], key=f"done_{i}")
                task["completed"] = done

            # Task display
            with col2:
                st.markdown(
                    f"""
                    <div style='padding:10px; border:1px solid #e5e7eb; border-radius:12px; margin-bottom:8px; background:#f9fafb;'>
                        <b>{task['title']}</b> 
                        <span style='background-color:#0f172a; color:white; padding:2px 8px; border-radius:8px; font-size:12px;'>
                            {task['priority'].upper()}
                        </span>  
                        📅 {task['due']}
                        <br>
                        <i>{task['notes'] if task['notes'] else ""}</i>
                        <div style='font-size:12px; color:#6b7280;'>
                            Added {task['created_at'].strftime('%Y-%m-%d %H:%M')}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Edit / Delete
            with col3:
                edit = st.button("✏️", key=f"edit_{i}")
                delete = st.button("🗑️", key=f"delete_{i}")
                if delete:
                    st.session_state.tasks.pop(i)
                    st.rerun()
