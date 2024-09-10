import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

def configure():
    load_dotenv()

load_dotenv()
LANGCHAIN_API_KEY=os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT=os.getenv("LANGCHAIN_PROJECT")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

os.environ["LANGCHAIN_TRACING_V2"]="true"

prompt_template=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please respond to the question asked"),
        ("user","Question:{question}")
    ]
)

st.set_page_config(page_title="Conversational AI chatbot", page_icon="🦜")
st.title(body="Conversational AI chatbot")
# input_text=st.text_input(label="What question you have in mind?")

if "messages" not in st.session_state:
    st.session_state['messages']=[
        {"role":"assistant","content":"Hi i am a AI powered conversational chatbot. How can i help you"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

if prompt:=st.chat_input(placeholder="What is machine learning?"):
    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)

    llm=ChatGroq(api_key=GROQ_API_KEY,model_name="Llama3-8b-8192")
    output_parser=StrOutputParser()
    chain=prompt_template|llm|output_parser

    with st.chat_message("assistant"):
        response=chain.invoke(st.session_state.messages)
        st.session_state.messages.append({'role':'assistant',"content":response})
        st.write(response)

