import streamlit as st

# Page title
st.set_page_config(page_title="AI To-Do List", page_icon="📝")
st.title("📝 AI To-Do List App")

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Add new task
new_task = st.text_input("Add a new task:")
if st.button("Add Task"):
    if new_task.strip() != "":
        st.session_state.tasks.append({"task": new_task, "done": False})
        st.experimental_rerun()

# Show tasks
st.subheader("Your Tasks")
for i, t in enumerate(st.session_state.tasks):
    col1, col2, col3 = st.columns([0.6, 0.2, 0.2])

    with col1:
        st.write("✅" if t["done"] else "⬜", t["task"])

    with col2:
        if st.button("Mark Done" if not t["done"] else "Undo", key=f"done{i}"):
            st.session_state.tasks[i]["done"] = not st.session_state.tasks[i]["done"]
            st.experimental_rerun()

    with col3:
        if st.button("❌ Delete", key=f"del{i}"):
            del st.session_state.tasks[i]
            st.experimental_rerun()
