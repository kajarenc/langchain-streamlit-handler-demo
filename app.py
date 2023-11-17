import streamlit as st
from langchain.llms import OpenAI


from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents import AgentType, initialize_agent
from customduckduckgo import CustomDuckDuckGoSearchRun

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

if not openai_api_key:
    st.sidebar.warning("Please provide OPENAI API key")
    openai_api_key = st.secrets["MY_OPENAI_API_KEY"]

llm = OpenAI(temperature=0, streaming=True, openai_api_key=openai_api_key)

tools = [CustomDuckDuckGoSearchRun()]
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(prompt, callbacks=[st_callback])
        st.write(response)