import chromadb
from .generate_embeddings import CodeEmbedding
from typing import List


class ChromaVectorStore:
    def __init__(self):
        self.persist_directory = "../db/chroma.db"

        self.chroma_client = chromadb.PersistentClient(
            path=self.persist_directory)

        self.graphrag_collection = self.chroma_client.get_or_create_collection(
            name="Graphrag-practice")

    def add_vector_to_collection(self, data: List[CodeEmbedding]):
        for vector in data:
            self.graphrag_collection.add(
                ids=vector.metadata["chunk_id"],
                embeddings=vector.vector_embedding,
                documents=vector.metadata["original_text_preview"],
                metadatas=vector.metadata
            )

        print(f"Vectors successfully added to collection")
        return
