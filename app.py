import streamlit as st
import datetime

st.set_page_config(page_title="To-Do App", page_icon="📝")
st.title("📝 To-Do App")

# --- Session State ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []


# --- Add Task ---
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


# --- Sidebar Filters & Sorting ---
st.sidebar.header("🔍 Filters & Sorting")

# Priority filter with "Select All"
all_priorities = ["low", "medium", "high"]
select_all = st.sidebar.checkbox("Select All Priorities", value=True)

if select_all:
    priority_filter = st.sidebar.multiselect(
        "Filter by Priority",
        all_priorities,
        default=all_priorities
    )
else:
    priority_filter = st.sidebar.multiselect(
        "Filter by Priority",
        all_priorities,
        default=[]
    )

# Date filter
date_range = st.sidebar.date_input(
    "Filter by Due Date Range",
    value=(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=30))
)

# Sorting
sort_by = st.sidebar.selectbox(
    "Sort By",
    ["due", "priority", "created_at"]
)
sort_order = st.sidebar.radio("Sort Order", ["Ascending", "Descending"])

# View toggle
view_option = st.sidebar.radio("View Tasks", ["Active", "Completed", "All"])


# --- Apply Filters ---
tasks = st.session_state.tasks

# Filter by priority
if priority_filter:
    tasks = [t for t in tasks if t["priority"] in priority_filter]

# Filter by date range
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    tasks = [t for t in tasks if start_date <= t["due"] <= end_date]

# Filter by status
if view_option == "Active":
    tasks = [t for t in tasks if not t["completed"]]
elif view_option == "Completed":
    tasks = [t for t in tasks if t["completed"]]


# --- Sorting ---
reverse = sort_order == "Descending"
tasks.sort(key=lambda x: x[sort_by], reverse=reverse)


# --- Show Tasks ---
st.subheader("Your Tasks")
if not tasks:
    st.info("No tasks to show with current filters.")
else:
    for i, task in enumerate(tasks, start=1):
        with st.container():
            col1, col2, col3 = st.columns([0.1, 6, 0.5])

            # Checkbox for completion
            with col1:
                done = st.checkbox("", value=task["completed"], key=f"done_{i}")
                task["completed"] = done

            # Task content
            with col2:
                st.markdown(
                    f"""
                    <div style='padding:12px; border:1px solid #e5e7eb; border-radius:12px; margin-bottom:8px; background:#f9fafb;'>
                        <b>{task['title']}</b>
                        <span style='background-color:#0f172a; color:white; padding:2px 8px; border-radius:8px; font-size:12px;'>
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

            # Edit / Delete
            with col3:
                edit = st.button("✏️", key=f"edit_{i}")
                delete = st.button("🗑️", key=f"delete_{i}")
                if delete:
                    st.session_state.tasks.remove(task)
                    st.rerun()
