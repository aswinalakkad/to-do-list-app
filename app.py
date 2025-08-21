import streamlit as st

st.set_page_config(page_title="To-Do List", page_icon="📝")
st.title("📝 Simple To-Do List")

# Initialize tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Input for new task
new_task = st.text_input("Add a new task:")

if st.button("➕ Add Task"):
    if new_task.strip() != "":
        st.session_state.tasks.append({"task": new_task, "done": False})
        st.experimental_rerun()

# Show task list
st.subheader("Your Tasks")
if len(st.session_state.tasks) == 0:
    st.info("No tasks yet! Add one above 👆")
else:
    for i, t in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([0.6, 0.2, 0.2])

        with col1:
            st.write("✅" if t["done"] else "⬜", t["task"])

        with col2:
            if st.button("✔️ Done" if not t["done"] else "↩️ Undo", key=f"done{i}"):
                st.session_state.tasks[i]["done"] = not st.session_state.tasks[i]["done"]
                st.experimental_rerun()

        with col3:
            if st.button("❌ Delete", key=f"del{i}"):
                del st.session_state.tasks[i]
                st.experimental_rerun()
