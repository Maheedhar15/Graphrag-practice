from .chunking import ChunkingStrategy
from Parsers.parser_selector import ParserSelector


class RecursiveChunking(ChunkingStrategy):
    def __init__(self):
        super().__init__()
        self._parser_selector = ParserSelector()

    def perform_chunking(self, data, language):
        chunker = self._parser_selector.get_parser(language=language)
        chunked_docs = chunker.create_documents([data])
        return (chunked_docs)
