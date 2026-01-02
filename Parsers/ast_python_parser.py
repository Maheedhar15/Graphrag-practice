import ast

from dataclasses import dataclass
from hashlib import sha256
from typing import List, Any, Dict


@dataclass
class CodeChunk:
    content: str
    metadata: Dict[str, Any]


class ASTPythonParser:
    def __init__(self):
        pass

    def create_documents(self, docs: List[str], file_path: str) -> List[CodeChunk]:
        source = docs[0]
        tree = ast.parse(source)
        lines = source.splitlines()

        chunks = []

        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                chunk = self._extract_code(node, lines)
                chunkid = self._generate_vector_id(
                    file_path=file_path, start_line=node.lineno, end_line=node.end_lineno)
                chunks.append(CodeChunk(
                    chunk_id=chunkid,
                    content=chunk,
                    metadata={
                        "type": "import",
                        "modules": self._extract_imports(node),
                        "start_line": node.lineno,
                        "end_line": node.end_lineno
                    }
                ))

        for node in tree.body:
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                chunk = self._extract_code(node, lines)
                chunkid = self._generate_vector_id(
                    file_path=file_path, start_line=node.lineno, end_line=node.end_lineno)
                chunks.append(CodeChunk(
                    chunk_id=chunkid,
                    content=chunk,
                    metadata={
                        "type": "constant",
                        "targets": self._extract_assign_targets(node),
                        "start_line": node.lineno,
                        "end_line": node.end_lineno
                    }
                ))

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                chunks.extend(self._process_function(node, lines, file_path))

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                chunks.extend(self._process_class(node, lines, file_path))

        return chunks

    # -------------------
    # Helper Functions
    # -------------------

    def _extract_code(self, node, lines):
        return "\n".join(lines[node.lineno - 1: node.end_lineno])

    def _extract_imports(self, node):
        if isinstance(node, ast.Import):
            return [alias.name for alias in node.names]
        if isinstance(node, ast.ImportFrom):
            return [f"{node.module}.{alias.name}" for alias in node.names]

        return []

    def _extract_assign_targets(self, node):
        if isinstance(node, ast.Assign):
            return [target.id for target in node.targets if isinstance(target, ast.Name)]
        if isinstance(node, ast.AnnAssign):
            return [node.target.id] if isinstance(node.target, ast.Name) else []
        return []

    def _process_function(self, node: ast.FunctionDef, lines, file_path) -> List[CodeChunk]:
        """Chunk for a standalone function."""
        chunk = self._extract_code(node, lines)
        chunkid = self._generate_vector_id(
            file_path=file_path, start_line=node.lineno, end_line=node.end_lineno)
        return [
            CodeChunk(
                chunk_id=chunkid,
                content=chunk,
                metadata={
                    "type": "function",
                    "name": node.name,
                    "args": [arg.arg for arg in node.args.args],
                    "decorators": [self._decorator_name(d) for d in node.decorator_list],
                    "start_line": node.lineno,
                    "end_line": node.end_lineno
                }
            )
        ]

    def _process_class(self, node: ast.ClassDef, lines, file_path) -> List[CodeChunk]:
        """Chunk for class + methods inside it."""
        chunks = []

        # Whole class chunk
        class_chunk = self._extract_code(node, lines)
        chunkid = self._generate_vector_id(
            file_path=file_path, start_line=node.lineno, end_line=node.end_lineno)
        chunk_id = self._generate_vector_id(
            file_path=file_path, start_line=node.lineno, end_line=node.end_lineno)

        Methods = []

        # Method chunks
        for child in node.body:
            if isinstance(child, ast.FunctionDef):
                chunkid = self._generate_vector_id(
                    file_path=file_path, start_line=child.lineno, end_line=child.end_lineno)
                method_chunk = self._extract_code(child, lines)
                chunks.append(CodeChunk(
                    chunk_id=chunkid,
                    content=method_chunk,
                    metadata={
                        "type": "method",
                        "name": child.name,
                        "class_name": node.name,
                        "args": [arg.arg for arg in child.args.args],
                        "decorators": [self._decorator_name(d) for d in child.decorator_list],
                        "start_line": child.lineno,
                        "end_line": child.end_lineno,
                    }
                ))
                Methods.append(chunkid)

        classChunk = CodeChunk(
            chunk_id=chunkid,
            content=class_chunk,
            metadata={
                "type": "class",
                "name": node.name,
                "bases": [self._get_base_name(b) for b in node.bases],
                "start_line": node.lineno,
                "end_line": node.end_lineno,
                "HAS_METHOD": Methods
            }
        )

        chunks.append(classChunk)

        return chunks

    def _decorator_name(self, dec):
        return getattr(dec, "id", getattr(dec, "attr", "unknown"))

    def _get_base_name(self, base):
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return base.attr
        return "unknown"

    def _generate_vector_id(self, file_path: str, start_line: int, end_line: int):
        line = f"{file_path}:{start_line}:{end_line}"
        encoded_line = sha256(line.encode("utf-8"))

        return encoded_line.hexdigest()
