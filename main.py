from typing import Set
import base64
from backend.core import run_llm
import streamlit as st
from streamlit_chat import message


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string

LOGO_IMAGE = "static/img/logo.png"

st.markdown(
    """
    <style>
    .container {
        display: flex;
    }
    .logo-text {
        font-weight:700 !important;
        font-size:40px !important;
        color: #fffff !important;
        padding-right: 20px

        
    }
    .logo-img {
        padding-top: 15px;
        float:right;
        width: 50px;
        height: 50px;
        
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="container">
    <p class="logo-text">EchoNexus</p>
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
        
    </div>
    """,
    unsafe_allow_html=True
)

if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []


prompt = st.text_input("Prompt", placeholder="Enter your message here...") or st.button(
    "Submit"
)

if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )

        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )
        formatted_response = (
            f"{generated_response['answer']} \n\n {create_sources_string(sources)}"
        )

        st.session_state.chat_history.append((prompt, generated_response["answer"]))
        st.session_state.user_prompt_history.append(prompt)
        st.session_state.chat_answers_history.append(formatted_response)

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        message(
            user_query,
            is_user=True,
            avatar_style="no-avatar",
            logo=None,
        )
        message(generated_response,
                avatar_style="bottts-neutral",
                seed="Casper",
                #logo='/opt/documentation-helper/static/img/eye.png',
                is_user=False,
                allow_html=True,
                )
