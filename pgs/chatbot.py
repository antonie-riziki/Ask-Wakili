
#!/usr/bin/env python3

import streamlit as st
import google.generativeai as genai
import os
import sys

sys.path.insert(1, './models')

from upload_file_rag import get_qa_chain, query_system

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(prompt):

    model = genai.GenerativeModel("gemini-1.5-flash", 

        system_instruction = '''

        You are 'Ask Wakili' Bot, a highly knowledgeable and professional legal assistant trained in both local (e.g., Kenyan) and international law. Your purpose is to assist users with questions 
        related only to these legal areas, including constitutional law, civil law, criminal law, human rights, administrative law, and international legal frameworks such as treaties, conventions, and global legal standards.

        If a user asks about topics outside the scope of law (such as medical advice, entertainment, relationships, or personal opinions), respond politely and conversationally, 
        reminding them that you are only able to assist with matters related to local and international law.

        Maintain a calm, respectful, and supportive tone. Use accessible legal language suitable for both legal professionals and the general public.

        🧠 Example Out-of-Scope Response:

        "I appreciate your curiosity! However, I'm specialized in legal matters and can only assist with questions related to local and international law. If you have any legal 
        concerns or need clarity on a legal issue, I’m here to help!"           


        ''')

    # Generate AI response

    response = model.generate_content(
        prompt,
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1, 
      )
    
    )


    
    return response.text


st.image('https://www.joengigiadvocates.co.ke/wp-content/uploads/2022/01/legal_consultancy.jpg', width=900)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])



if prompt := st.chat_input("How may I help?"):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    chat_output = get_gemini_response(prompt)
    
    # Append AI response
    with st.chat_message("assistant"):
        st.markdown(chat_output)

    st.session_state.messages.append({"role": "assistant", "content": chat_output})

# pdf_path = "ConstitutionofKenya 2010.pdf"
# print(pdf_path)
# qa_chain = get_qa_chain(pdf_path)
# print('This is the qa section', qa_chain)


# # Initialize session state for chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# # Display chat history
# for message in st.session_state.messages:

#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])


# if prompt := st.chat_input("How may I help?", key='RAG chat'):
#     # Append user message
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Generate AI response
#     chat_output = query_system(prompt, qa_chain)
    
#     # Append AI response
#     with st.chat_message("assistant"):
#         st.markdown(chat_output)

#     st.session_state.messages.append({"role": "assistant", "content": chat_output})