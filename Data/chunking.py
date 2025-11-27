import abc
from abc import abstractmethod


class ChunkingStrategy(abc):
    def __init__(self):
        pass

    @classmethod
    @abstractmethod
    def perform_chunking(self, data, language):
        pass
