import streamlit as st
import google.generativeai as palm
from streamlit_chat import message
from langdetect import detect
from googletrans import Translator

palm.configure(api_key="AIzaSyDXX6-9lzWrfqbWJmzHTAjmFmex0hqMv6Y")
translator = Translator()

defaults = {
    'model': 'models/chat-bison-001',
    'temperature': 0.25,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
}

context = "Sports Assistant: Provide instructions or ask questions about sports, and I will provide useful information or advice."

st.set_page_config(page_title="Chatbot")

def initiate(prompt_input):
    answer = palm.chat(
        **defaults,
        context=context,
        messages=[prompt_input]
    )
    return answer.last

def reply(prev_msg, user_input):
    answer = palm.chat(
        **defaults,
        context=context,
        messages=[prev_msg, user_input]
    )
    return answer.last

def get_language(text):
    try:
        language = detect(text)
        return language
    except:
        return 'en'
    
def translate_prompt(lang, text):
    translated_response = translator.translate(text, src=lang, dest='en').text
    return translated_response

def translated_response(lang, text):
    translated_response = translator.translate(text, src='en', dest=lang).text
    return translated_response

st.title("Sports")
st.sidebar.markdown("# Chatbot")

if st.sidebar.button("Clear Session"):
    st.session_state.chat_history = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if prompt := st.chat_input():
    full_prompt = f'Provide instructions or ask questions about sports is {prompt}'
    user_language = get_language(prompt)
    user_prompt = translate_prompt(user_language, prompt)

    if not st.session_state.chat_history:
        answer = initiate(user_prompt)
    else:
        prev_msg = st.session_state.chat_history[-1]
        answer = reply(prev_msg, user_prompt)
    

    st.session_state.chat_history.append(f'You: {prompt}')  

    if answer is not None:
        user_respon = translated_response(user_language, answer)
        st.session_state.chat_history.append(f'AI: {user_respon}')
    else:
        st.session_state.chat_history.append("AI: I'm sorry, I couldn't understand or answer that question. Please try another one.")

for i, chat_entry in enumerate(st.session_state.chat_history):
    
    if "You:" in chat_entry:
        message(chat_entry, is_user=True, key=f"user_{i}")
    elif "AI:" in chat_entry:
        message(chat_entry, key=f"ai_{i}")