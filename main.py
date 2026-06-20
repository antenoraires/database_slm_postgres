from src.pipeline import Pipeline

import os
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv

from minio import Minio
from src.ingest.ingest_minio import inserir_arquivo, ler_bytes, listar_caminhos

load_dotenv()

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

#path_local = "assents/rsl_antenor.pdf"
path_local = "assents/WMamba.pdf"

BUCKET_NAME = "documentos"

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # True em produção (HTTPS)
)

# inserindo arquivo
inserir_arquivo(client, path_local, BUCKET_NAME, os.path.basename(path_local))
print ("Arquivo enviado com sucesso!")

# Processa um PDF que já está armazenado no MinIO
dados_pdf = ler_bytes(client, BUCKET_NAME, os.path.basename(path_local))
with NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
    tmp.write(dados_pdf)
    caminho_temp = tmp.name

p = Pipeline()
p.processar_documento(caminho_temp, tipo="pdf", titulo=os.path.basename(path_local))

# lista = listar_caminhos(client, BUCKET_NAME, prefixo="")
# print(lista)

# Busca inteligente
resultados = p.buscar("Qual a universidade com mais destaque nos estudos sobre deepfake?", top_k=3)

for r in resultados:
    print(f"Score: {r['similaridade']:.3f}")
    print(f"Trecho: {r['texto'][:300]}...\n")