from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from pgvector.sqlalchemy import Vector
from datetime import datetime

from src.config import DATABASE_URL

Base = declarative_base()



class Documento(Base):
    """Tabela principal para textos brutos"""
    __tablename__ = "documentos"
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(255))
    fonte = Column(String(500))          # URL, nome do arquivo, etc.
    texto_completo = Column(Text)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Documento(id={self.id}, titulo='{self.titulo}')>"

class Embedding(Base):
    """Tabela vetorial para busca semântica"""
    __tablename__ = "embeddings"
    
    id = Column(Integer, primary_key=True)
    documento_id = Column(Integer)       # FK para documentos
    chunk_texto = Column(Text)           # Trecho do texto
    embedding = Column(Vector(384))      # Dimensão do MiniLM-L12-v2
    #embedding = Column(Vector(768))
    posicao_chunk = Column(Integer)      # Ordem do chunk no documento

# Cria as tabelas (rode uma vez)
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.commit()

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)