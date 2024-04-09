# MultiPDF ChatMaster
An LLM-based chatbot to assist you with multiple PDFs of your choice
Access it here [MultiPDF ChatMaster URL](https://pdfchatting01.streamlit.app/)

## App Architecture / Logic

We use FAISS (Facebook AI Similarity Search), though it shows Pinecone in the architecture.
<img width="1294" alt="image" src="https://github.com/DeepankDixit/chat-with-multiple-pdfs/assets/22991058/c24f5c97-e271-4d28-acd9-edfc334a6425">

## How it works

Here's how the app works to answer your questions:
1. **Document Loading (PDFs Loading)**: It takes in one or several PDF files and extracts the text content from them.
2. **Document Splitting**: This text is then split into smaller chunks using LangChain's RecursiveCharacterTextSplitter.
3. **Embedding using OpenAI and FAISS**: The app uses OpenAIEmbeddings for the chunk embeddings and FAISS index for locally preparing the vector store.
4. **Q&A through Similarity Search**: The app retrieves the relevant chunks from the vector store when the user asks something. Relevant chunks are the ones that are closest in meaning to your question.
5. **Send Query to LLM and Response**: It then uses these extracted text chunks along with the user query to the OpenAI language model to synthesize an answer based on the relevant content of the PDF.

### Installing the Dependencies

1. Clone the repository to your local machine
2. Run `pip install -r requirements.txt` to install the required dependencies
3. Get your OpenAI API key and save it in the `.env` file in the project directly
`OPENAI_API_KEY="your_secret_api_key"`

## How to run it locally

1. Run the `main.py` file from the project directly using `streamlit run app.py`
2. This will launch the app in your web browser
3. You can load multiple PDFs and click on Process. 
4. Once the processing is complete, you can ask questions in natural language about the PDFs


