import os
from dotenv import load_dotenv

from minio import Minio
from src.ingest.ingest_minio import inserir_arquivo, ler_bytes, listar_caminhos

load_dotenv()

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

path_local = "assents/rsl_antenor.pdf"

BUCKET_NAME = "documentos"

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # True em produção (HTTPS)
)

# in erindo arquivo
#inserir_arquivo(client, path_local, BUCKET_NAME, "rsl_antenor.pdf")
#print ("Arquivo enviado com sucesso!")
lista = listar_caminhos(client, BUCKET_NAME, prefixo="")
print(lista)