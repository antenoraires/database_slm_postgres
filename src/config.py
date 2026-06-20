import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:senha123@localhost:5432/meu_banco"
)

# Modelo de embedding (multilíngue, leve e eficiente)
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Tamanho dos chunks de texto
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50