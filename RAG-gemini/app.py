import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai

from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def pdf_text(pdf_docs):
    text = ''
    for pdf  in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def chunker(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size = 10000, chunk_overlap = 1000)
    chunks = splitter.split_text(text)
    return chunks

def vec_store(chunks):
    embedding = GoogleGenerativeAIEmbeddings(model='models/embedding-001')
    store = FAISS.from_texts(chunks, embedding = embedding)
    store.save_local('faiss_index')  
    
def get_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    
    model = ChatGoogleGenerativeAI(model= 'gemini-pro', temperature=0.3)
    
    prompt = PromptTemplate(template= prompt_template, input_variables=['context', 'question'])
    
    chain = load_qa_chain(model, chain_type='stuff', prompt = prompt)
    
    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001')
    print(embeddings.embed_query('hello my friend')[0:5])
    new_db = FAISS.load_local("./faiss_index", embeddings) 
    docs = new_db.similarity_search(query=user_question)

    chain = get_chain()

    
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    print(response)
    st.write("Reply: ", response["output_text"])




def main():
    st.set_page_config("Chat PDF")
    st.header("Chat with PDF using Gemini💁")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = pdf_text(pdf_docs)
                text_chunks = chunker(raw_text)
                vec_store(text_chunks)
                st.success("Done")



if __name__ == "__main__":
    main()