import streamlit as st
import datetime

st.set_page_config(page_title="To-Do App", page_icon="📝")

st.title("📝 To-Do App")

# Session state to store tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Add new task
with st.form("add_task"):
    title = st.text_input("Task Title")
    notes = st.text_area("Notes")
    due = st.date_input("Due Date", datetime.date.today())
    priority = st.selectbox("Priority", ["low", "medium", "high"])
    submitted = st.form_submit_button("Add Task")

    if submitted and title:
        st.session_state.tasks.append({
            "title": title,
            "notes": notes,
            "due": due,
            "priority": priority,
            "created_at": datetime.datetime.now(),
            "completed": False
        })

# Filters
st.subheader("Filters & Sorting")
col1, col2 = st.columns(2)

with col1:
    priority_filter = st.selectbox("Filter by Priority", ["All", "low", "medium", "high"])

with col2:
    sort_option = st.selectbox("Sort by", ["Due Date", "Priority"])

# Apply filter
tasks = st.session_state.tasks
if priority_filter != "All":
    tasks = [task for task in tasks if task["priority"] == priority_filter]

# Apply sorting
if sort_option == "Due Date":
    tasks = sorted(tasks, key=lambda x: x["due"])
elif sort_option == "Priority":
    priority_order = {"high": 1, "medium": 2, "low": 3}
    tasks = sorted(tasks, key=lambda x: priority_order[x["priority"]])

# Show tasks
st.subheader("Your Tasks")
for i, task in enumerate(tasks):
    col1, col2, col3 = st.columns([0.1, 0.7, 0.2])

    # Checkbox for completion
    with col1:
        if st.checkbox("", value=task["completed"], key=f"complete_{i}"):
            st.session_state.tasks[i]["completed"] = True
        else:
            st.session_state.tasks[i]["completed"] = False

    # Task content
    with col2:
        if task["completed"]:
            title_display = f"""
                <span style="
                    text-decoration: line-through;
                    text-decoration-thickness: 2px;
                    text-decoration-color: #ef4444;
                    text-decoration-skip-ink: none;
                    text-decoration-offset: 3px;
                ">
                    {task['title']}
                </span>
            """
        else:
            title_display = task["title"]

        st.markdown(
            f"""
            <div style='padding:12px; border:1px solid #e5e7eb; border-radius:12px; margin-bottom:8px; background:#f9fafb;'>
                <b>{title_display}</b>
                <span style='background-color:#6b7280; color:white; padding:2px 8px; border-radius:8px; font-size:12px;'>
                    {task['priority'].upper()}
                </span>
                📅 {task['due']}
                <br>
                <div style='margin-top:4px; font-size:14px;'>{task['notes'] if task['notes'] else ""}</div>
                <div style='font-size:12px; color:#6b7280;'>
                    Added {task['created_at'].strftime('%Y-%m-%d %H:%M')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Delete button
    with col3:
        if st.button("🗑️ Delete", key=f"delete_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()
