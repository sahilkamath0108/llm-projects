import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers

def get_ans(input_text, num_words, blog_style):
    llm = CTransformers(model = 'C:\\Users\\Hp\\Desktop\\llama-2-7b-chat.ggmlv3.q8_0.bin',
                        model_type = 'llama',
                        config = {'max_new_tokens' : 256,
                                  'temperature' : 0.01})
    
    template = """
        Write a blog for {style} job profile for a topic {text}
        within {n_words} words.
    """
    
    prompt = PromptTemplate(input_variables=['style', 'text', 'n_words'],
                            template=template)
    
    resp = llm(prompt.format(style = blog_style, text = input_text, n_words = num_words))
    print(resp)
    return resp

st.set_page_config('Generate Blogs')

st.header("Generate Blogs")

input_text = st.text_input("Enter blog topic")

col1, col2 = st.columns([5,5])
with col1:
    num_words = st.text_input("Number of words: ")
    
with col2:
    blog_style = st.selectbox("Writing the blog for ", ("Researcher", "Data Scientist", "Common People"), index=0)
    
submit = st.button('Generate')

if submit:
    st.write(get_ans(input_text, num_words, blog_style))