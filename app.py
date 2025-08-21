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
        background-color: #374151;
        color: white;
        padding: 3px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        margin-left: 8px;
    }
    .completed {
        text-decoration: line-through;
        text-decoration-thickness: 2px;
        text-decoration-color: #ef4444;
        text-decoration-offset: 3px;
    }
    .segmented-control button {
        margin-right: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("To-Do ✨")

# --- Session State ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "view" not in st.session_state:
    st.session_state.view = "All"



# --- Add Task ---
with st.container():
    with st.form("add_task", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            title = st.text_input("Task title", label_visibility="collapsed")
        with col2:
            due = st.date_input("Due date", datetime.date.today(), label_visibility="collapsed")

        notes = st.text_area("Notes (optional)", label_visibility="collapsed")
        col3, col4 = st.columns([1, 3])
        with col3:
            priority = st.selectbox("Priority", ["low", "medium", "high"])
        with col4:
            tags = st.text_input("Tags: work, personal")

        submitted = st.form_submit_button("➕ Add", use_container_width=True)

        if submitted and title:
            st.session_state.tasks.append({
                "title": title,
                "notes": notes,
                "due": due,
                "priority": priority,
                "tags": tags,
                "created_at": datetime.datetime.now(),
                "completed": False
            })

# --- Segmented Control for Views ---
colA, colB, colC, colD, colE = st.columns([1, 1, 1, 2, 2])

with colA:
    if st.button("All", use_container_width=True):
        st.session_state.view = "All"
with colB:
    if st.button("Active", use_container_width=True):
        st.session_state.view = "Active"
with colC:
    if st.button("Completed", use_container_width=True):
        st.session_state.view = "Completed"
with colD:
    if st.button("Clear completed", use_container_width=True):
        st.session_state.tasks = [t for t in st.session_state.tasks if not t["completed"]]
with colE:
    if st.button("Reset", use_container_width=True):
        st.session_state.tasks = []

search = st.text_input("🔍 Search tasks", label_visibility="collapsed")

# --- Filter & Search ---
tasks = st.session_state.tasks

if st.session_state.view == "Active":
    tasks = [t for t in tasks if not t["completed"]]
elif st.session_state.view == "Completed":
    tasks = [t for t in tasks if t["completed"]]

if search:
    tasks = [t for t in tasks if search.lower() in t["title"].lower()]

# --- Show Tasks ---
st.subheader("Your Tasks")
if not tasks:
    st.info("No tasks match. Try adding one above ✍️")
else:
    for i, task in enumerate(tasks):
        with st.container():
            col1, col2, col3 = st.columns([0.1, 7, 0.5])
            with col1:
                done = st.checkbox("", value=task["completed"], key=f"done_{i}")
                st.session_state.tasks[i]["completed"] = done
            with col2:
                title_class = "completed" if task["completed"] else ""
                st.markdown(
                    f"""
                    <div class="task-card">
                        <span class="{title_class}"><b>{task['title']}</b></span>
                        <span class="priority-pill">{task['priority'].upper()}</span>
                        📅 {task['due']}
                        <div style="margin-top:6px; font-size:14px;">{task['notes']}</div>
                        <div style="font-size:12px; color:#6b7280;">
                            Added {task['created_at'].strftime('%Y-%m-%d %H:%M')}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col3:
                if st.button("🗑️", key=f"delete_{i}"):
                    st.session_state.tasks.remove(task)
                    st.rerun()

