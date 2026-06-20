from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL
import numpy as np

class EmbeddingGenerator:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
    
    def gerar(self, textos: list[str]) -> np.ndarray:
        """Gera embeddings para uma lista de textos"""
        return self.model.encode(textos, show_progress_bar=True)
    
    def gerar_unico(self, texto: str) -> np.ndarray:
        """Gera embedding para um único texto"""
        return self.model.encode(texto)