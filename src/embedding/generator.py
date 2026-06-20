from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL
import numpy as np

import re
from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL
import numpy as np

class EmbeddingGenerator:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def _normalize(self, texto: str) -> str:
        texto = re.sub(r'\s+', ' ', texto).strip()
        return texto

    def gerar(self, textos: list[str]) -> np.ndarray:
        textos = [self._normalize(t) for t in textos]
        return self.model.encode(
            textos,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    def gerar_unico(self, texto: str) -> np.ndarray:
        texto = self._normalize(texto)
        return self.model.encode(
            texto,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

# class EmbeddingGenerator:
#     def __init__(self):
#         self.model = SentenceTransformer(EMBEDDING_MODEL)
    
#     def gerar(self, textos: list[str]) -> np.ndarray:
#         """Gera embeddings para uma lista de textos"""
#         return self.model.encode(textos, show_progress_bar=True)
    
#     def gerar_unico(self, texto: str) -> np.ndarray:
#         """Gera embedding para um único texto"""
#         return self.model.encode(texto)