from typing import List

class TextChunker:
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk(self, texto: str) -> List[str]:
        """Divide texto em chunks com sobreposição"""
        palavras = texto.split()
        chunks = []
        
        i = 0
        while i < len(palavras):
            chunk = palavras[i:i + self.chunk_size]
            chunks.append(" ".join(chunk))
            i += self.chunk_size - self.overlap
        
        return chunks