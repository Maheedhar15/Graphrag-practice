import os
import sys
from pathlib import Path

# Add parent directory to path to import Data module
sys.path.insert(0, str(Path(__file__).parent.parent))


class KnowledgegraphBuilder:
    def __init__(self, chunking_strategy):
        from Data.chunking_selector import ChunkingStrategySelector
        self.chunking_strategy = ChunkingStrategySelector(
            chunking_strategy=chunking_strategy)

    def get_chunks(self, data, language):
        self.chunking_strategy.chunk_data(data=data, language=language)


if __name__ == "__main__":
    data_path = "../Project-data"
    supported_extensions = [".py", ".js", ".jsx"]

    for root, dirs, files in os.walk(data_path):
        print(f"{root} {dirs} {files}")
