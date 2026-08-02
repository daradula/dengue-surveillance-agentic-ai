import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DOCS_PATH = "data/documents"
VECTORSTORE_PATH = "rag/vectorstore"

# Step 1: Load all PDFs
print("Loading documents...")
documents = []
for filename in os.listdir(DOCS_PATH):
    if filename.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(DOCS_PATH, filename))
        documents.extend(loader.load())
print(f"Loaded {len(documents)} pages from PDFs")

# Step 2: Chunk documents
print("Splitting into chunks...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

# Step 3: Create embeddings + store in Chroma
print("Creating embeddings and vector store...")
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=VECTORSTORE_PATH
)
print(f"Vector store saved to {VECTORSTORE_PATH}")