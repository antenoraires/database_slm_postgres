from minio import Minio
from minio.error import S3Error
import io



def inserir_arquivo(client: Minio, caminho_local: str, 
                    BUCKET_NAME: str, nome_no_minio: str,
                    metadata: dict[str, str] | None = None):
    """
    Envia um arquivo do disco para o MinIO.

    metadata: dicionário opcional para armazenar metadados customizados.
    """
    # validar bucket
    if not client.bucket_exists(BUCKET_NAME):
        client.make_bucket(BUCKET_NAME)
        print(f"Bucket '{BUCKET_NAME}' criado.")

    client.fput_object(
        bucket_name=BUCKET_NAME,
        object_name=nome_no_minio,
        file_path=caminho_local,
        content_type="application/pdf",  # ajuste conforme o tipo
        metadata=metadata or {}
    )
    print(f"Arquivo '{nome_no_minio}' enviado com sucesso.")


def ler_bytes(client: Minio, BUCKET_NAME: str, nome_no_minio: str) -> bytes:
    """
    Lê arquivo do MinIO direto em memória (sem salvar no disco).
    Útil para passar ao PyPDF2, etc.
    """
    resposta = client.get_object(BUCKET_NAME, nome_no_minio)
    return resposta.read()


def obter_metadados(client: Minio, BUCKET_NAME: str, nome_no_minio: str) -> dict[str, str]:
    """
    Retorna os metadados do objeto no MinIO sem baixar o conteúdo.
    """
    stat = client.stat_object(BUCKET_NAME, nome_no_minio)
    return stat.metadata or {}


def listar_caminhos(
    client: Minio,
    bucket: str,
    prefixo: str = "",
    recursivo: bool = False
) -> list[str]:
    """
    Lista caminhos de arquivos em uma pasta do MinIO.
    
    prefixo: pasta no bucket, ex: "2024/", "contratos/"
    recursivo: True inclui subpastas, False so a pasta atual
    """
    
    caminhos = []
    
    objetos = client.list_objects(
        bucket_name=bucket,
        prefix=prefixo,
        recursive=recursivo
    )
    
    for obj in objetos:
        # pula objetos de diretorio (pastas vazias)
        if obj.object_name.endswith("/"):
            continue
        caminhos.append(f"{bucket}/{obj.object_name}")
    
    return caminhos