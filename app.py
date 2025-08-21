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
        col1, col2, col3 = st.columns([5, 2, 2])

        with col1:
            st.markdown(f"**{task['title']}** (priority: {task['priority']}, due: {task['due']})")
            st.caption(f"Added {task['created_at'].strftime('%Y-%m-%d %H:%M')}")
            if task["notes"]:
                st.write(f"📝 {task['notes']}")

        with col2:
            if st.button(f"{'✅ Undo' if task['completed'] else '✔️ Done'} {i}"):
                task["completed"] = not task["completed"]
                st.rerun()

        with col3:
            if st.button(f"🗑️ Delete {i}"):
                st.session_state.tasks.remove(task)
                st.rerun()
