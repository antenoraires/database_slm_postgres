import sqlalchemy
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:senha123@localhost:5432/meu_banco"
)

engine = sqlalchemy.create_engine(DATABASE_URL)

class DummyGenerator:
    def gerar(self, textos):
        return np.array([[0.1]*384 for _ in textos])

    def gerar_unico(self, texto):
        return np.array([0.1]*384)


class DummyEmbedding:
    def __init__(self, documento_id, chunk_texto, embedding, posicao_chunk):
        self.documento_id = documento_id
        self.chunk_texto = chunk_texto
        self.embedding = embedding
        self.posicao_chunk = posicao_chunk
