import streamlit as st
import openai
import os

# Set page config
st.set_page_config(page_title="AI To-Do List", page_icon="🤖📝")
st.title("🤖📝 AI-Powered To-Do List")

# Get API key (from Streamlit secrets or input)
if "OPENAI_API_KEY" not in st.secrets:
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
else:
    api_key = st.secrets["OPENAI_API_KEY"]

if api_key:
    openai.api_key = api_key

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

# AI Suggestions Section
st.subheader("🤖 AI Task Suggestions")
if api_key:
    if st.button("✨ Suggest Tasks"):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant suggesting daily tasks."},
                    {"role": "user", "content": "Suggest 5 useful tasks for today in bullet points."}
                ],
                max_tokens=150
            )
            ai_tasks = response["choices"][0]["message"]["content"].split("\n")
            st.write("Here are some ideas:")
            for t in ai_tasks:
                if t.strip():
                    if st.button(f"Add: {t}", key=f"ai{t}"):
                        st.session_state.tasks.append({"task": t, "done": False})
                        st.experimental_rerun()
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.warning("Enter your OpenAI API key above to get AI task suggestions.")
