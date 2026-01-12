import streamlit as st
from openai import OpenAI
from google import genai
from groq import Groq

from core.config import config

def run_llm(provider, model_name, messages, max_tokens=500):
    if provider == "openai":
        client = OpenAI(api_key=config.openai_api_key)
    elif provider == "google":
        client = genai.Client(api_key=config.google_api_key)
    elif provider == "groq":
        client = Groq(api_key=config.groq_api_key)
    else:
        raise ValueError(f"Invalid provider: {provider}")

    
    if provider == "google":
        return client.models.generate_content(
            model=model_name,
            contents=[message["content"] for message in messages],
        ).text
    elif provider == "groq":
        return client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_completion_tokens=max_tokens,
        ).choices[0].message.content
    else:
        return client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_completion_tokens=max_tokens,
            reasoning_effort="minimal",
        ).choices[0].message.content    

with st.sidebar:
    st.title("Settings")
    
    
    provider = st.selectbox("Select a provider", ["openai", "google", "groq"])
    
    if provider == "openai":
        model_name = st.selectbox("Select a model", ["gpt-5-nano", "gpt-5-mini"])
    elif provider == "google":
        model_name = st.selectbox("Select a model", ["gemini-2.5-flash"])
    elif provider == "groq":
        model_name = st.selectbox("Select a model", ["llama-3.3-70b-versatile"])
    else:
        model_names = st.selectbox("Select a model", ["gemini-2.5-flash", "llama-3.3-70b-versatile"])

    st.session_state.provider = provider
    st.session_state.model_name = model_name

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello, how can I help you today?"}]
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hello, how can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        output = run_llm(st.session_state.provider, st.session_state.model_name, st.session_state.messages)
        response_data = output
        answer = response_data
        st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

