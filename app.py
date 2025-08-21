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

    if submitted:
        if title.strip():
          st.session_state.tasks.append({
            "title": title,
            "notes": notes,
            "due": due,
            "priority": priority,
            "created_at": datetime.datetime.now()
          })
          st.success("Task added!")
          st.rerun()   # ✅ new rerun method
        else:
          st.warning("⚠️ Please enter a task title before adding.")
# Show tasks
st.subheader("Your Tasks")
if not st.session_state.tasks:
    st.info("No tasks yet. Add one above ⬆️")
else:
    for i, task in enumerate(st.session_state.tasks):
        # ✅ Use .get() to avoid KeyError
        title = task.get("title", "Untitled")
        priority = task.get("priority", "medium")
        due = task.get("due", "N/A")
        created = task.get("created_at", datetime.datetime.now())

        st.markdown(f"**{title}** (priority: {priority}, due: {due})")
        st.caption(f"Added {created.strftime('%Y-%m-%d %H:%M')}")

        if st.button(f"Delete {i}"):
            st.session_state.tasks.pop(i)
            st.rerun()


