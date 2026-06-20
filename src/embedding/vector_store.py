from sqlalchemy.orm import Session
from src.database.models import Embedding, SessionLocal
from src.embedding.generator import EmbeddingGenerator
import numpy as np

class VectorStore:
    def __init__(self):
        self.generator = EmbeddingGenerator()
    
    def inserir_chunks(self, documento_id: int, chunks: list[str]):
        """Gera embeddings e salva no banco vetorial"""
        embeddings = self.generator.gerar(chunks)
        
        session = SessionLocal()
        try:
            for i, (chunk, vetor) in enumerate(zip(chunks, embeddings)):
                emb = Embedding(
                    documento_id=documento_id,
                    chunk_texto=chunk,
                    embedding=vetor.tolist(),
                    posicao_chunk=i
                )
                session.add(emb)
            session.commit()
        finally:
            session.close()
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        a = np.asarray(a, dtype=float)
        b = np.asarray(b, dtype=float)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    def buscar_similar(self, query: str, top_k: int = 5):
        """Busca semanticamente no banco vetorial"""
        vetor_query = self.generator.gerar_unico(query)
        
        session = SessionLocal()
        try:
            # Busca por similaridade de cosseno no banco
            resultados = session.query(Embedding).order_by(
                Embedding.embedding.cosine_distance(vetor_query)
            ).limit(top_k).all()
            
            return [
                {
                    "texto": r.chunk_texto,
                    "documento_id": r.documento_id,
                    "similaridade": self._cosine_similarity(vetor_query, np.asarray(r.embedding))
                }
                for r in resultados
            ]
        finally:
            session.close()