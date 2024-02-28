import streamlit as st
from dotenv import load_dotenv

load_dotenv()
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel(model_name='gemini-pro')

def gemini(q):
    resp = model.generate_content(q)
    return resp.text

st.set_page_config(page_title="Q&A Demo")

st.header("Gemini Application")

input=st.text_input("Input: ",key="input")


submit=st.button("Ask the question")

if submit:
    
    response = gemini(input)
    st.subheader("The Response is")
    st.write(response)