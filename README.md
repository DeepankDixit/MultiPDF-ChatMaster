![image](https://github.com/DeepankDixit/MultiPDF-ChatMaster/assets/22991058/0a384560-89be-416d-bc33-b670b234b2fd)![image](https://github.com/DeepankDixit/MultiPDF-ChatMaster/assets/22991058/98750491-8651-4137-80b6-4cfa9a53af0b)An LLM-based chatbot to assist you with multiple PDFs of your choice.

Access it here [MultiPDF ChatMaster URL](https://multipdf-chatmaster.streamlit.app/)

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

1. Run the `app.py` file from the project directly using `streamlit run app.py`
2. This will launch the app in your web browser
3. You can load multiple PDFs and click on Process. 
4. Once the processing is complete, you can ask questions in natural language about the PDFs

## App walkthrough

1. App UI
<img width="1299" alt="image" src="https://github.com/DeepankDixit/MultiPDF-ChatMaster/assets/22991058/a7b73530-ed4e-40ea-b1b7-c06b25e3b224">


2. Upload the PDFs (supports multiple PDFs) with which you want to chat. I am using ISE 3.2 CLI Reference Guide, and a completely different PDF about Cisco's acquisition of a company called Isovalent.

[CISCO ACQUIRES ISOVALENT](https://nand-research.com/wp-content/uploads/2024/01/2024-01-18-Cisco-Isovalent-Acquisition.pdf), and [Cisco Identity Services Engine CLI Reference Guide](https://www.cisco.com/c/en/us/td/docs/security/ise/3-2/cli_guide/b_ise_CLI_Reference_Guide_32/b_ise_CLIReferenceGuide_32_chapter_01.html)

Click on "Process".

<img width="1173" alt="image" src="https://github.com/DeepankDixit/MultiPDF-ChatMaster/assets/22991058/b971d22e-0f3c-4938-82f4-fd00e338d06e">

Wait until Processing is complete. 

<img width="1291" alt="image" src="https://github.com/DeepankDixit/MultiPDF-ChatMaster/assets/22991058/9456adcf-72ad-4845-8a67-362b30119258">

Chatbot is now active.

3. Enter your queries and engage in the conversation. Remember that the bot has memory and will remember the conversation exchanged during an entire session.

e.g., "I got locked out of ISE because of attempting to login using an incorrect password. How can I reset my password? For “admin” user"

<img width="1205" alt="image" src="https://github.com/DeepankDixit/MultiPDF-ChatMaster/assets/22991058/689e0836-9cd9-4b62-8927-ebf2c36d568f">

"What is this Isovalent acquisition all about? How does it help cisco. List in bullet points"

<img width="1109" alt="image" src="https://github.com/DeepankDixit/MultiPDF-ChatMaster/assets/22991058/5f7936be-b834-4fd2-80d3-7accb97a2894">

"At what valuation was the deal closed?" 

<img width="986" alt="image" src="https://github.com/DeepankDixit/MultiPDF-ChatMaster/assets/22991058/bdd9a710-ea33-467b-9038-be9dae9ed1f2">

(Note that the model didn't hallucinate and made up some information on the valuation of the company)





