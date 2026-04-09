import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {"configurable": {"thread_id": "thread-1"}}

st.title("Chatbot")

# session state
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

# Display previous messages
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:

    # Save user message
    st.session_state["message_history"].append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    # AI response container
    with st.chat_message("assistant"):

        response_container = st.empty()
        streamed_text = ""

        for event in chatbot.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode="updates"
        ):

            for node_output in event.values():
                if "messages" in node_output:
                    streamed_text += node_output["messages"][-1].content
                    response_container.markdown(streamed_text + "▌")

        # Save final response
        st.session_state["message_history"].append(
            {"role": "assistant", "content": streamed_text}
        )

        response_container.markdown(streamed_text)