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

# 🔍 Search filter
search_query = st.sidebar.text_input("Search by Title/Notes").lower()

# --- Display Tasks ---
for i, task in enumerate(st.session_state.tasks):
    if (task["priority"] in priority_filter and
        date_range[0] <= task["due"] <= date_range[1] and
        (search_query in task["title"].lower() or search_query in task["notes"].lower())):
        
        st.write(f"**{task['title']}** - {task['notes']} (📅 {task['due']}, 🔑 {task['priority']})")
