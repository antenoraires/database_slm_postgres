from src.pipeline import Pipeline

import os
from dotenv import load_dotenv

from minio import Minio
from src.ingest.ingest_minio import ingest_documento, listar_caminhos, listar_arquivos_pasta

load_dotenv()

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
  
BUCKET_NAME = "documentos"
pasta_local = "assents"  

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # True em produção (HTTPS)
)

# iniciando pipeline
p = Pipeline()

for path_local in listar_arquivos_pasta(pasta_local):
    resultado = ingest_documento(
        client,
        path_local,
        BUCKET_NAME,
        nome_no_minio=os.path.basename(path_local),
        tipo= "pdf" if path_local.lower().endswith('.pdf') else "txt",
        titulo=os.path.basename(path_local),
        metadata={
            "x-amz-meta-origem": "upload-usuario",
            "x-amz-meta-tipo": "documento"
        },
        salvar_txt_em=f"assents/backup/{os.path.splitext(os.path.basename(path_local))[0]}.txt"
    )
    print("Upload + ingestão concluídos:", resultado)

# Busca inteligente
resultados = p.buscar("rostos gerados por GAN?", top_k=5)

for r in resultados:
    print(f"Score: {r['similaridade']:.3f}")
    print(f"Trecho: {r['texto'][:300]}...\n")