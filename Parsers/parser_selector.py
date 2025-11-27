from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter
)


class ParserSelector:
    def __init__(self):
        self._language = "python"
        self._parser = None

    def set_parser(self, language="python", chunk_size=5000, chunk_overlap=0):

        if language == "python":
            self._parser = RecursiveCharacterTextSplitter.from_language(
                language=Language.PYTHON, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        else:
            self._parser = RecursiveCharacterTextSplitter.from_language(
                language=Language.JS, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def get_parser(self, language):

        self.set_parser(language=language)
        return self._parser
