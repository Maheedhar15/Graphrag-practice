from agentic_chunking import AgenticChunking
from recursive_chunking import RecursiveChunking


class ChunkingStrategySelector:
    def __init__(self, chunking_strategy="Agentic"):
        if chunking_strategy == "Agentic":
            self._chunking_strategy = AgenticChunking()
        else:
            self._chunking_strategy = RecursiveChunking()

    def set_chunking_strategy(self, chunking_strategy="Agentic"):
        if chunking_strategy == "Agentic":
            self._chunking_strategy = AgenticChunking()
        else:
            self._chunking_strategy = RecursiveChunking()

    def chunk_data(self, data, language):
        self._chunking_strategy.perform_chunking(data=data, language=language)
