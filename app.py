#Chat with multiple PDFs

import time
import streamlit as st
from PyPDF2 import PdfReader
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv
from bs4 import BeautifulSoup
load_dotenv()


def get_reponse(user_question):
    response = st.session_state.conversation({'question': user_question}) #remember: st.session_state.conversation chain already contains all of the config from our vector store and from our memory
    # st.write(response)
    return response['answer']


def get_vectorstore_from_pdf(pdf_docs):

    with st.sidebar:
        with st.spinner('Loading the document...'):
            # document loading
            text = ""
            for pdf in pdf_docs:
                pdf_reader = PdfReader(pdf)
                for page in pdf_reader.pages:
                    text += page.extract_text()
                # time.sleep(1)
        st.success('Document loaded!', icon="✅")
        # st.write(document[0])

    with st.sidebar:
        with st.spinner('Splitting the document into chunks...'):
            #document chunking
            text_splitter = RecursiveCharacterTextSplitter(
                separators=["\n\n", "\n", ".", ","],
                chunk_size=2000,
                chunk_overlap=500,
                length_function=len
            )
            chunks = text_splitter.split_text(text)
            document_chunks = text_splitter.create_documents(chunks)
            # time.sleep(1)
        st.success(f'Document chunking completed! {len(chunks)} chunks', icon="✅")

    with st.sidebar:
        with st.spinner('Creating vectorstore from document chunks...'):
            #creating embeddings from documents and storing in vectorstore
            embeddings = OpenAIEmbeddings()
            vector_store = Chroma.from_documents(document_chunks, embeddings) #two args: 1: doc chunks, 2: embeddings
            # time.sleep(1)
        st.success('Embeddings created and saved to vectorstore', icon="✅")
        st.info("This vector store will take care of storing embedded data and perform vector search for you.")
    
    return vector_store

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(temperature=0)
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

# app config
st.set_page_config(page_title="ISE Chat Assistant for PDFs", page_icon="🔐")
st.title("ISE Chat Assistant for PDFs :books:")

with st.sidebar:
    st.subheader("Your documents")
    pdf_docs = st.file_uploader(
        "Upload your PDFs here and click on Process", accept_multiple_files=True)
    process_button = st.button("Process")

if pdf_docs == []:
    st.info("Please upload the PDFs, then click on Process")
    print("pdf_docs currently is empty: ", pdf_docs)

else:
    if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                AIMessage(content="Hello, I am a bot. How can I help you?")
            ]   
    if "conversation" not in st.session_state:
            st.session_state.conversation = None

    if "vector_store" not in st.session_state:
            st.session_state.vector_store = None
    
    #track if st.button("Process") is clicked
    if "button_clicked" not in st.session_state:
         st.session_state.button_clicked = 0

    if process_button: 
        st.session_state.button_clicked = 1
        print("button clicked!")
        #build the vectorstore from PDFs
        st.session_state.vector_store = get_vectorstore_from_pdf(pdf_docs)

    if st.session_state.button_clicked == 1:
        #user input
        user_query = st.chat_input("Type your message here...")
        print(f"user_query: {user_query}")
        if user_query is not None and user_query != "":
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            response = get_reponse(user_query)
            st.session_state.chat_history.append(AIMessage(content=response))

        # show the HumanMessage and AIMessage as conversation on the webpage
        for message in st.session_state.chat_history:
            # st.write(st.session_state.chat_history)
            if isinstance(message, AIMessage):
                with st.chat_message("AI"):
                    st.markdown(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message("Human"):
                    st.markdown(message.content)

        #create conversation chain
        st.session_state.conversation = get_conversation_chain(st.session_state.vector_store)
