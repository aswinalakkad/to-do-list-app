import streamlit as st
import datetime

st.title("📝 To-Do App with Filters & Sorting")

# --- Session state ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- Add Task Form ---
with st.form("add_task", clear_on_submit=True):
    title = st.text_input("Task Title")
    notes = st.text_area("Notes")
    due = st.date_input("Due Date", datetime.date.today())
    priority = st.selectbox("Priority", ["low", "medium", "high"])
    submitted = st.form_submit_button("Add Task")

    if submitted:
        if title.strip():
            st.session_state.tasks.append({
                "title": title,
                "notes": notes,
                "due": due,
                "priority": priority,
                "created_at": datetime.datetime.now(),
                "completed": False
            })
            st.success("Task added!")
            st.rerun()
        else:
            st.warning("⚠️ Please enter a task title before adding.")

# --- Tabs for Active / Completed ---
tab1, tab2 = st.tabs(["📌 Active Tasks", "✅ Completed Tasks"])

# === Sidebar Filters & Sorting ===
st.sidebar.header("🔍 Filters & Sorting")

priority_filter = st.sidebar.multiselect(
    "Filter by Priority",
    ["low", "medium", "high"],
    default=["low", "medium", "high"]
)

date_range = st.sidebar.date_input(
    "Filter by Due Date Range",
    value=(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=30))
)

sort_by = st.sidebar.selectbox(
    "Sort By",
    ["due", "priority", "created_at"]
)

sort_order = st.sidebar.radio("Sort Order", ["Ascending", "Descending"])

# --- Helper: filter & sort ---
def filter_and_sort(tasks):
    filtered = [t for t in tasks if t["priority"] in priority_filter]

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range
        filtered = [t for t in filtered if start <= t["due"] <= end]

    reverse = (sort_order == "Descending")

    if sort_by == "priority":
        # custom sort: low < medium < high
        priority_order = {"low": 0, "medium": 1, "high": 2}
        filtered.sort(key=lambda t: priority_order[t["priority"]], reverse=reverse)
    else:
        filtered.sort(key=lambda t: t[sort_by], reverse=reverse)

    return filtered

# --- Active Tasks ---
with tab1:
    active_tasks = filter_and_sort([t for t in st.session_state.tasks if not t["completed"]])
    if not active_tasks:
        st.info("No active tasks 🎉")
    else:
        for i, task in enumerate(active_tasks, start=1):
            st.markdown(f"**{i}. {task['title']}** (priority: {task['priority']}, due: {task['due']})")
            st.caption(f"Added {task['created_at'].strftime('%Y-%m-%d %H:%M')}")
            c1, c2 = st.columns(2)
            if c1.button(f"✅ Mark Done {i}", key=f"done_{i}"):
                idx = st.session_state.tasks.index(task)
                st.session_state.tasks[idx]["completed"] = True
                st.rerun()
            if c2.button(f"🗑️ Delete {i}", key=f"del_active_{i}"):
                idx = st.session_state.tasks.index(task)
                st.session_state.tasks.pop(idx)
                st.rerun()

# --- Completed Tasks ---
with tab2:
    completed_tasks = filter_and_sort([t for t in st.session_state.tasks if t["completed"]])
    if not completed_tasks:
        st.info("No completed tasks yet ✅")
    else:
        for i, task in enumerate(completed_tasks, start=1):
            st.markdown(f"~~{i}. {task['title']}~~ (priority: {task['priority']}, due: {task['due']})")
            st.caption(f"Completed {task['created_at'].strftime('%Y-%m-%d %H:%M')}")
            c1, c2 = st.columns(2)
            if c1.button(f"↩️ Mark Active {i}", key=f"undo_{i}"):
                idx = st.session_state.tasks.index(task)
                st.session_state.tasks[idx]["completed"] = False
                st.rerun()
            if c2.button(f"🗑️ Delete {i}", key=f"del_done_{i}"):
                idx = st.session_state.tasks.index(task)
                st.session_state.tasks.pop(idx)
                st.rerun()
