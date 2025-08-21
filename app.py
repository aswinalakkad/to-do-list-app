import streamlit as st
import datetime

st.set_page_config(page_title="To-Do App", page_icon="📝")

st.title("📝 To-Do App")

# Session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Add task form
with st.form("add_task", clear_on_submit=True):
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
st.sidebar.header("Filters & Sort")
priority_filter = st.sidebar.selectbox("Priority", ["All", "low", "medium", "high"])
sort_by = st.sidebar.selectbox("Sort by", ["Created Time", "Due Date", "Priority"])

# Apply filters
filtered_tasks = st.session_state.tasks
if priority_filter != "All":
    filtered_tasks = [t for t in filtered_tasks if t["priority"] == priority_filter]

# Apply sorting
if sort_by == "Due Date":
    filtered_tasks = sorted(filtered_tasks, key=lambda x: x["due"])
elif sort_by == "Priority":
    priority_order = {"high": 0, "medium": 1, "low": 2}
    filtered_tasks = sorted(filtered_tasks, key=lambda x: priority_order[x["priority"]])
else:
    filtered_tasks = sorted(filtered_tasks, key=lambda x: x["created_at"], reverse=True)

st.subheader("Your Tasks")

# Show tasks in card format
for i, task in enumerate(filtered_tasks):
    with st.container():
        col1, col2, col3 = st.columns([0.1, 4, 0.5])

        with col1:
            done = st.checkbox("", value=task["completed"], key=f"done_{i}")
            st.session_state.tasks[i]["completed"] = done

        with col2:
            st.markdown(
                f"**{task['title']}** "
                f"<span style='background-color:#0f172a; color:white; padding:2px 8px; border-radius:8px; font-size:12px;'>{task['priority'].upper()}</span> "
                f"📅 {task['due']}",
                unsafe_allow_html=True,
            )
            if task["notes"]:
                st.write(task["notes"])
            st.caption(f"Added {task['created_at'].strftime('%Y-%m-%d %H:%M')}")

        with col3:
            edit = st.button("✏️", key=f"edit_{i}")
            delete = st.button("🗑️", key=f"delete_{i}")
            if delete:
                st.session_state.tasks.pop(i)
                st.rerun()
