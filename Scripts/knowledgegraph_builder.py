import os
import sys
from pathlib import Path
from pprint import pprint

# Add parent directory to path to import Data module
sys.path.insert(0, str(Path(__file__).parent.parent))


class KnowledgegraphBuilder:
    def __init__(self, chunking_strategy):
        from Data.chunking_selector import ChunkingStrategySelector
        self.chunking_strategy = ChunkingStrategySelector(
            chunking_strategy=chunking_strategy)

    def get_chunks(self, data, language):
        chunks = self.chunking_strategy.chunk_data(
            data=data, language=language)
        return chunks


if __name__ == "__main__":
    data_path = "../Project-data"
    supported_extensions = {".py": "python"}

    kgb = KnowledgegraphBuilder(chunking_strategy="recursive")

    for root, dirs, files in os.walk(data_path):
        for file in files:
            file_path = Path(root) / file
            file_ext = file_path.suffix
            if file_ext in supported_extensions:
                language = supported_extensions[file_ext]
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    data = f.read()

                print(f"Parsing File: {file_path}\n\n\n")
                chunks = kgb.get_chunks(data, language.lower())
                pprint(chunks)
                break
