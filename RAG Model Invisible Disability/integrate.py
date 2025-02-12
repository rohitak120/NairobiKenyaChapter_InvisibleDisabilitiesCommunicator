import streamlit as st
from langchain_community.document_loaders.csv_loader import CSVLoader
from pathlib import Path
import os
from dotenv import load_dotenv

import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_groq import ChatGroq 
from langchain_community.embeddings import HuggingFaceEmbeddings 

import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Load environment variables from a .env file
load_dotenv()

# Set the OpenAI API key environment variable
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

llm = ChatGroq(model="deepseek-r1-distill-llama-70b")

# Path to the CSV file in the current directory
csv_file_path = Path("temp_matatu_routes.csv")

# Load and split CSV file documents
loader = CSVLoader(file_path=csv_file_path)
docs = loader.load_and_split()

# Initiate faiss vector store and huggingface embedding
embeddings = HuggingFaceEmbeddings()
index = faiss.IndexFlatL2(len(HuggingFaceEmbeddings().embed_query(" ")))
vector_store = FAISS(
    embedding_function=HuggingFaceEmbeddings(),
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={}
)

vector_store.add_documents(documents=docs)

retriever = vector_store.as_retriever()

# Set up system prompt
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If the context does not contain relevant "
    "information, respond with 'I do not know'.  Do not add "
    "any extra information beyond what is in the retrieved "
    "context. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# Create the question-answer chain
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

def main():
    # Custom CSS for styling
    st.markdown(
        """
        <style>
        /* Remove default padding and margin */
        html, body, .stApp {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
        }

        /* Full-width background gradient */
        .stApp {
            background: linear-gradient(to right, #74ebd5, #acb6e5);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        /* Full-width output window */
        .output-window {
            background-color: #ffffff;
            padding: 20px;
            border: 1px solid #cccccc;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            width: 90%; /* Use 90% of the screen width */
            height: 300px; /* Increased height */
            overflow-y: auto;
            margin: 20px auto; /* Center alignment */
            text-align: left;
        }

        /* Full-width input section */
        .input-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 20px;
            width: 90%; /* Use 90% of the screen width */
            margin-left: auto;
            margin-right: auto;
        }

        /* Input box styling */
        .input-box {
            background-color: #ffffff;
            padding: 10px;
            border: 1px solid #cccccc;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            margin-bottom: 10px; /* Space between input box and button */
        }

        /* Submit button styling */
        .submit-button {
            background-color: #00698f;
            color: #ffffff;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 200px; /* Adjust the width as needed */
        }

        .submit-button:hover {
            background-color: #003d5c;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Title Section
    st.markdown("<h1 style='text-align: center; font-size: 50px; color: #003d5c;'>Invisible Disability Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; color: #444;'>Nairobi Disability Support Platform</p>", unsafe_allow_html=True)

    # Output Window
    output_window = st.empty()  # Placeholder for dynamic output
    with output_window.container():
        st.markdown("<div class='output-window'>Output will be displayed here...</div>", unsafe_allow_html=True)

    # Input and Submit Button Section
    query = st.text_input("", placeholder="Type your query here", key="input-field")
    if st.button("Submit", key="submit-button"):
        if query:
            try:
                response = rag_chain.invoke({"input": query})
                output_window.markdown(f"<div class='output-window'>{response['answer']}</div>", unsafe_allow_html=True)
            except Exception as e:
                output_window.markdown(f"<div class='output-window'>Error: {e}</div>", unsafe_allow_html=True)
        else:
            output_window.markdown("<div class='output-window'>Please enter a query!</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()