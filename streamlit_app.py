import streamlit as st

from app.agent import agent
from utils import add_message, display_tool_calls

st.title("Chatbot")
st.write(
    "Este é um chatbot que usa IA (yaaaay). "
    "Para utilizá-lo, você precisa disponibilizar uma chave de API da OpenAI API, que você pode obter [aqui](https://platform.openai.com/account/api-keys)."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt := st.chat_input("O que você gostaria de saber?"):
    add_message("user", prompt)

for message in st.session_state["messages"]:
    if message["role"] in ["user", "assistant"]:
        content = message["content"]
        if content is not None:
            with st.chat_message(message["role"]):
                if "tool_calls" in message and message["tool_calls"]:
                    display_tool_calls(st.empty(), message["tool_calls"])
                st.markdown(content)

last_message = (
    st.session_state["messages"][-1] if st.session_state["messages"] else None
)
if last_message and last_message.get("role") == "user":
    question = last_message["content"]

    with st.chat_message("assistant"):
        tool_calls_container = st.empty()
        resp_container = st.empty()
        with st.spinner("..."):
            response = ""
            try:
                run_response = agent.run(question, stream=True)
                for _resp_chunk in run_response:
                    if _resp_chunk.tools and len(_resp_chunk.tools) > 0:
                        display_tool_calls(tool_calls_container, _resp_chunk.tools)

                    if _resp_chunk.content is not None:
                        response += _resp_chunk.content
                        resp_container.markdown(response)

                add_message(
                    "assistant",
                    response,
                    agent.run_response.tools if agent.run_response else [],
                )
            except Exception as e:
                error_message = f"Desculpe, parece que aconteceu um erro: {str(e)}"
                add_message("assistant", error_message)
                st.error(error_message)
