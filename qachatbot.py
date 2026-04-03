# Simple Langchain Stream lit App with Groq
# A Beginner-Friendly version focusing on core concepts

import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
import os

# Page configuration

st.set_page_config(page_title="Simple Lang Chain Chat bot with Groq", page_icon='🚀')

# Title
st.title("🚀 Simple LangChain Chatbot  with Groq")
st.markdown("Learn LangChain basics with Groq's ultra-fast inference!")

with st.sidebar:
    st.header("Settings")

    ## API Key 
    api_key= st.text_input("OpenAI API Key", type="password",help="Get Free API key at platform.openai.com")

    ## Model Selection
    model_name= st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o"],
        index=0
    )

    # Clear Button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    

    ## Intialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages =[]

    ## Intialize LLM
    @st.cache_resource
    
    def get_chain(api_key, model_name):
        if not api_key:
            return None
        
        # Intialize LLM Groq Model
        llm = ChatOpenAI(openai_api_key = api_key,
                 model_name= model_name,
                 temperature=0.7
                 ,
                 streaming=True)
        
        # Create Prompt Template
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant powered by Groq. Answer questions clearly and conciesly."),
            ("user", "{question}")
        ])

        # Create Chain
        chain = prompt | llm| StrOutputParser()

        return chain
    
    # Get Chain
    chain = get_chain(api_key, model_name)

    if not chain:
        st.warning("Please enter your Groq api in the side bar to start chatting!")
        st.markdown("Get your free api key here ")
    else:
        # Display the chat messages.

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])



    # Chat Input
    if question:= st.chat_input("Ask me anything:"):
        # Add user message to session state
        st.session_state.messages.append({"role":"user","content":question})
        with st.chat_message("user"):
            st.write(question)


     # Generate Response:
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = " "

    try:
        #stream response from Groq:
        for chunk in chain.stream({"question": question}):
            full_response += chunk
            message_placeholder.markdown(full_response + "")
        message_placeholder.markdown(full_response)    

        # Add to history
        st.session_state.messages.append({"role": "assistant","content": full_response})

    except Exception as e:
        st.error(f"Error : {str(e)}")

#Examples:
st.markdown("---")   
st.markdown("### Try these Examples:") 
col1, col2=st.columns(2)       
with col1:
    st.markdown("- What is LangChain?")
    st.markdown("- Explain Groq's LPU technology")
with col2:
    st.markdown("- how do I Learn Programming?")
    st.markdown("- Write a haiku about AI")

# Footer
st.markdown("---")    
st.markdown("Built with Lang Chain and Grok | Exprience the Speed!")


           
                


