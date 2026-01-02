from openai import OpenAI
from Parsers.ast_python_parser import CodeChunk
from typing import List, Any, Dict

from dataclasses import dataclass


@dataclass
class CodeEmbedding:
    vector_embedding: str
    metadata: Dict[str, Any]


class EmbedCode:
    def __init__(self):
        self.embedding_model = "text-embedding-bge-m3"
        self.embedding_client = OpenAI(
            base_url="http://localhost:1234/v1", api_key="lm-studio")

    def generate_embeddings(self, chunks: List[CodeChunk], file_path: str):
        vectors = []
        # print(chunks)
        for chunk in chunks:
            text = chunk.content.replace("\n", " ")
            vector_embedding = self.embedding_client.embeddings.create(
                input=[text], model=self.embedding_model).data[0].embedding

            vector_metadata = {
                "chunk_id": chunk.chunk_id,
                "file_path": str(file_path),
                "start_line": chunk.metadata["start_line"],
                "end_line": chunk.metadata["end_line"],
                "node_type": chunk.metadata["type"],
                "original_text_preview": chunk.content[:40],
                "embedding_model": self.embedding_model
            }

            vector = CodeEmbedding(
                vector_embedding=vector_embedding, metadata=vector_metadata)

            vectors.append(vector)
        return vectors
