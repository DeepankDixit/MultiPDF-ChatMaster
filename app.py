import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from htmlTemplates import css, bot_template, user_template

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
#"""to avoid this error: OMP: Error #15: Initializing libomp.dylib, but found libiomp5.dylib already initialized.
#OMP: Hint This means that multiple copies of the OpenMP runtime have been linked into the program"""


#func to return single string of text from all of the pdfs
def get_pdf_text(pdf_docs): 
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", ","],
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings() #you pay for this. OpenAI charges. Pretty Fast
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl") #Free but way slower (Note: causes kernel crash in my pc)
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question}) #remember: st.session_state.conversation chain already contains all of the config from our vector store and from our memory
    # st.write(response)
    st.session_state.chat_history = response['chat_history']
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    # st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    load_dotenv()

    st.write(css, unsafe_allow_html=True)

    #initializing the session state variable as best practice
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history"  not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents: ")

    if user_question:
        handle_userinput(user_question)
    
    st.write(user_template.replace("{{MSG}}", "Hello bot!"), unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}", "Hello human!"), unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on Process", accept_multiple_files=True)
        
        if st.button("Process"): #button will become True only when the user clicks on it
            with st.spinner("Processing"): #all the contents inside the spinner happens while the user sees "Processing" (makes user friendly)
                #get the pdf text (raw content): Doc loading manually using PyPDF2
                raw_text = get_pdf_text(pdf_docs)
                # st.write(raw_text) #for testing

                #get the text chunks: Doc splitting using LangChain
                text_chunks = get_text_chunks(raw_text)
                # st.write(text_chunks)

                #create vector store/ knowlege base
                vectorstore = get_vectorstore(text_chunks) 

                #create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)
                
                # """Q. How to make your variable persistent during the entire lifecycle of your application:
                # The thing about streamlit is that: whenever some click or any action takes place on the webapp, it reloads the whole code.
                # which causes all variables to be reinitialized. If I don't want that to happen and make sure that some variables are persistent, then you can make a variable 'var' persistent by doing st.session_state.var. This way, the var is linked to the session state of the app, and app knows that this var is not supposed to be re-initialized."""

                # """st.session_state.var is also useful when you have a var that's supposed to be used for the entire application"""

                # """Good practice to initialize the session_state variables at the top. Check top! Through this way, you can use this anywhere in the application.. not just inside the scope of 'with' """




if __name__ == '__main__':
    main()
