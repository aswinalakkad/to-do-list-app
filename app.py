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
