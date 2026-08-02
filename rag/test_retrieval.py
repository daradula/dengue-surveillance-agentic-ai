from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

VECTORSTORE_PATH = "rag/vectorstore"

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory=VECTORSTORE_PATH, embedding_function=embedding_model)

# 5 sample queries relevant to your domain
test_queries = [
    "What are the symptoms of severe dengue?",
    "How does rainfall affect dengue transmission in Colombo?",
    "What vector control measures are recommended by WHO?",
    "What is the relationship between ENSO and dengue outbreaks?",
    "How is dengue risk mapped spatially in Jaffna?"
]

for query in test_queries:
    print(f"\n{'='*60}")
    print(f"QUERY: {query}")
    print('='*60)
    results = vectorstore.similarity_search(query, k=3)
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get("source", "unknown")
        print(f"\n[Result {i}] Source: {source}")
        print(doc.page_content[:300])