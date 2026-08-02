from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


class KnowledgeAgent:

    def __init__(self, vectorstore_path="rag/vectorstore"):

        # Load embedding model
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Load existing Chroma vector store
        self.vectorstore = Chroma(
            persist_directory=vectorstore_path,
            embedding_function=self.embedding_model
        )

    def retrieve(self, query, k=3):

        # Retrieve most relevant chunks
        results = self.vectorstore.similarity_search(
            query=query,
            k=k
        )

        retrieved_chunks = []

        # Convert LangChain Documents to simple dictionaries
        for doc in results:

            retrieved_chunks.append(
                {
                    "source": doc.metadata.get("source", "Unknown"),
                    "content": doc.page_content
                }
            )

        return retrieved_chunks


# ----------------------------------------------------
# Example Usage
# ----------------------------------------------------
if __name__ == "__main__":

    agent = KnowledgeAgent()

    query = (
        "Dengue prevention guidelines for high rainfall "
        "and increasing dengue cases in Colombo."
    )

    results = agent.retrieve(query, k=3)

    for i, item in enumerate(results, start=1):
        print(f"\nResult {i}")
        print(f"Source : {item['source']}")
        print(f"Content: {item['content']}")