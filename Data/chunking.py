import abc
from abc import ABC, abstractmethod


class ChunkingStrategy(ABC):
    def __init__(self):
        pass

    @classmethod
    @abstractmethod
    def perform_chunking(self, data, language):
        pass
