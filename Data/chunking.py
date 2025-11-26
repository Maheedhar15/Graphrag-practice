import abc
from abc import abstractmethod


class ChunkingStrategy(abc):
    @classmethod
    @abstractmethod
    def perform_chunking(self, data):
        pass
