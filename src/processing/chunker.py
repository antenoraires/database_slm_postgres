import re
from typing import List

class TextChunker:
    SENTENCE_RE = re.compile(r'(?<=[.!?])\s+|\n+')

    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, texto: str) -> List[str]:
        texto = " ".join(texto.split())
        sentences = self.SENTENCE_RE.split(texto)
        chunks = []
        current = []

        for sentence in sentences:
            words = sentence.split()
            if not words:
                continue

            if len(current) + len(words) <= self.chunk_size:
                current.extend(words)
                continue

            if current:
                chunks.append(" ".join(current))
                current = current[-self.overlap:]

            if len(words) > self.chunk_size:
                start = 0
                while start < len(words):
                    end = min(start + self.chunk_size, len(words))
                    chunks.append(" ".join(words[start:end]))
                    if end == len(words):
                        break
                    start = max(end - self.overlap, start + 1)
                current = []
            else:
                current = words

        if current:
            chunks.append(" ".join(current))

        return chunks