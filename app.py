import streamlit as st
import datetime

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
            "created_at": datetime.datetime.now()
        })

# Show tasks
st.subheader("Your Tasks")
for i, task in enumerate(st.session_state.tasks):
    st.markdown(f"**{task['title']}** (priority: {task['priority']}, due: {task['due']})")
    st.caption(f"Added {task['created_at'].strftime('%Y-%m-%d %H:%M')}")
    if st.button(f"Delete {i}"):
        st.session_state.tasks.pop(i)
        st.experimental_rerun()
