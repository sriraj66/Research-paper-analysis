import os
import queue
import tempfile
import threading
import streamlit as st
from cred import *
from embedchain import App
from embedchain.helpers.callbacks import generate
import dotenv

dotenv.load_dotenv()

api_key = os.getenv("OPEN_API_KEY")

def embedchain_bot(db_path, api_key):
    return App.from_config(
        config={
            "llm": {
                "provider": "openai",
                "config": {
                    "model": "gpt-4o-mini",
                    "temperature": 0.5,
                    "max_tokens": 1000,
                    "top_p": 1,
                    "stream": True,
                    "api_key": api_key,
                },
            },
            "vectordb": {
                "provider": "chroma",
                "config": {"collection_name": "chat-pdf", "dir": db_path, "allow_reset": True},
            },
            "embedder": {"provider": "openai", "config": {"api_key": api_key}},
            "chunker": {"chunk_size": 2000, "chunk_overlap": 0, "length_function": "len"},
        }
    )

def get_db_path():
    tmpdirname = tempfile.mkdtemp()
    return tmpdirname

def get_ec_app(api_key):
    if "app" in st.session_state:
        app = st.session_state.app
    else:
        db_path = get_db_path()
        app = embedchain_bot(db_path, api_key)
        st.session_state.app = app
    return app

# Sidebar for uploading PDFs
with st.sidebar:

    title = st.title(TEAM_NAME)

    pdf_files = st.file_uploader("Upload your PDF files", accept_multiple_files=True, type="pdf")
    add_pdf_files = st.session_state.get("add_pdf_files", [])
    app = get_ec_app(api_key)

    for pdf_file in pdf_files:
        file_name = pdf_file.name
        if file_name in add_pdf_files:
            continue
        try:
            temp_file_name = None
            with tempfile.NamedTemporaryFile(mode="wb", delete=False, prefix=file_name, suffix=".pdf") as f:
                f.write(pdf_file.getvalue())
                temp_file_name = f.name
            if temp_file_name:
                st.markdown(f"Adding {file_name} to knowledge base...")
                app.add(temp_file_name, data_type="pdf_file")
                add_pdf_files.append(file_name)
                os.remove(temp_file_name)
            st.session_state.messages.append({"role": "assistant", "content": f"Added {file_name} to knowledge base!"})
        except Exception as e:
            st.error(f"Error adding {file_name} to knowledge base: {e}")
    st.session_state["add_pdf_files"] = add_pdf_files

def display_sidebar():
    sidebar_content = """
    <h2 style="font-size: 18px; color: #007bff;">Team Members</h2>
    <ul style="list-style-type: none; padding-left: 0;">"""

    for i in TEAM_METES:
        sidebar_content+=f"<li><strong>{i[0]}</strong> - Register Number: {i[1]}</li>"
    
    sidebar_content+="</ul>"

    st.sidebar.markdown(sidebar_content, unsafe_allow_html=True)

display_sidebar()


st.title(PROJECT_TITLE)
st.markdown(
    f'<p style="font-size: 17px; color: #aaa;">{PROJECT_DESCRIPTION}</p>',
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """
                Hi! I'm your Research Helper. I can help you analyze and discuss research papers. I can also help you in conducting research.
                Upload your PDF documents, and ask me any questions about them. I can handle up to 100 pages per PDF!
            """,
        },
        {
            "role": "assistant",
            "content": """
                Please note: If you provide input unrelated to research or document-related work, I will kindly ignore it and focus on assisting you with research.
            """,
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything!"):
    app = get_ec_app(api_key)


    with st.chat_message("user"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.markdown(prompt)

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        msg_placeholder.markdown("Typing...")
        full_response = ""

        q = queue.Queue()

        def app_response():
            try:
                result = app.chat(prompt, citations=False)
                if isinstance(result, tuple):
                    answer = result[0] 
                else:
                    answer = result 
                q.put(answer)
            except Exception as e:
                q.put(str(e))


        thread = threading.Thread(target=app_response)
        thread.start()

        while thread.is_alive() or not q.empty():
            while not q.empty():
                answer_chunk = q.get()
                full_response += answer_chunk
                msg_placeholder.markdown(full_response)

        thread.join()

        msg_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

