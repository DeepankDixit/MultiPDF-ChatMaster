An LLM-based chatbot to assist you with multiple PDFs of your choice
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
<img width="1394" alt="image" src="https://github.com/DeepankDixit/MultiPDF-ChatMaster/assets/22991058/bab8193f-6e21-4bca-86a5-2e00afca29da">

2. Upload the PDFs (supports multiple PDFs) with which you want to chat. I am using ISE 3.2 Installation Guide, and a completely different PDF about Cisco's acquisition of a company called Isovalent.

[CISCO ACQUIRES ISOVALENT](https://nand-research.com/wp-content/uploads/2024/01/2024-01-18-Cisco-Isovalent-Acquisition.pdf), and [Cisco Identity Services Engine Installation Guide, Release 3.2](https://www.cisco.com/c/en/us/td/docs/security/ise/3-2/install_guide/b_ise_installationGuide32.pdf)

Click on "Process".

<img width="1393" alt="image" src="https://github.com/DeepankDixit/MultiPDF-ChatMaster/assets/22991058/ad328a25-04c6-413c-87e4-4d5614510217">

Wait until Processing is complete. 

3. Enter your queries and engage in the conversation. Remember that the bot has memory and will remember the conversation exchanged during an entire session.

e.g., "I got locked out of ISE because of attempting to login using an incorrect password. That was all I had. How can I fix this?"

<img width="1038" alt="image" src="https://github.com/DeepankDixit/MultiPDF-ChatMaster/assets/22991058/75dfb00f-e69f-4113-b971-3e0721856c2d">

"I am logged in the ISE cli, wanna verify the system health and config of the deployment"

<img width="1156" alt="image" src="https://github.com/DeepankDixit/MultiPDF-ChatMaster/assets/22991058/302daf61-a648-46db-9145-9959c732110a">

"What is this acquisition all about? How does it help cisco. List in bullet points"

<img width="1148" alt="image" src="https://github.com/DeepankDixit/MultiPDF-ChatMaster/assets/22991058/0858f102-6f98-4802-8c9c-c4e73707dc5b">

"At what valuation was the deal closed?" 

<img width="966" alt="image" src="https://github.com/DeepankDixit/MultiPDF-ChatMaster/assets/22991058/143592b3-9e81-4823-afe4-ed25c27f9b78">
(Note that the model didn't hallucinate and made up some information on the valuation of the company)





