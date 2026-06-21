# Database SLM com PostgreSQL

Uma implementação simples de um pipeline de busca semântica usando PostgreSQL com `pgvector` como banco vetorial.

## O que o projeto faz

- extrai texto de PDFs, URLs e arquivos TXT
- divide o texto em chunks
- gera embeddings usando `sentence-transformers`
- armazena documentos no PostgreSQL e embeddings no `pgvector`
- pesquisa semanticamente em conteúdos processados
- envia arquivos para MinIO e processa documentos a partir do storage

## Estrutura do projeto

- `main.py` - exemplo de uso do pipeline e ingestão de documentos
- `src/pipeline.py` - fluxo principal de processamento e busca
- `src/processing/` - extração e chunking de texto
- `src/ingest/` - integração com MinIO e helpers de ingestão
- `src/embedding/` - geração de embeddings e pesquisa vetorial
- `src/database/` - modelos SQLAlchemy e inicialização do banco
- `src/config.py` - configuração do banco e modelo de embeddings
- `docker-compose.yml` - serviço PostgreSQL com `pgvector`

## Requisitos

- Python 3.12+
- Docker (recomendado para PostgreSQL)
- Dependências Python no `requirements.txt` ou `pyproject.toml`
- MinIO (opcional, mas usado pelo pipeline de ingestão)

## Variáveis de ambiente

Defina as variáveis de ambiente para acessar o MinIO e o banco:

- `MINIO_ENDPOINT` - endpoint do MinIO (por exemplo `localhost:9000`)
- `MINIO_ACCESS_KEY` - access key do MinIO
- `MINIO_SECRET_KEY` - secret key do MinIO

Exemplo em `.env`:

```env
MINIO_ENDPOINT=
MINIO_ACCESS_KEY=
MINIO_SECRET_KEY=
```

## Instalação

1. Crie e ative o ambiente virtual

```bash
cd /Users/aires/Downloads/projetos/database_slm_postgres
uv init
uv venv
source .venv/bin/activate
uv sync
```

2. Instale as dependências (optativo)

```bash
pip install -r requirements.txt
```

3. Inicie o banco PostgreSQL com `pgvector`

```bash
docker compose up -d
```

4. Confirme se o container está rodando

```bash
docker compose ps
```

## Uso básico

Execute o script principal:

```bash
python main.py
```

Ou, se você usa `uv`:

```bash
uv run python main.py
```

### API de busca com FastAPI

O projeto também expõe uma página web e um endpoint de busca via FastAPI.

- `GET /` mostra um formulário simples para enviar perguntas.
- `POST /search` executa `p.buscar(...)`.

#### Validação do endpoint `/search`

O FastAPI valida o payload antes de executar a busca:

- `query` deve ter entre 3 e 300 caracteres.
- `top_k` deve ser um inteiro entre 1 e 20.

Exemplo de uso :

```bash
uvicorn src.api:app --reload
```


```bash
curl -X POST http://127.0.0.1:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "rostos gerados por GAN?", "top_k": 5}'
```

### Ingestão de arquivos

O projeto agora suporta uma função de ingestão que:

1. envia o arquivo local para o MinIO
2. processa o documento no pipeline
3. salva o texto extraído opcionalmente em `.txt`

Exemplo de uso direto em Python:

```python
from src.ingest.ingest_minio import ingest_documento

resultado = ingest_documento(
    client,
    "assents/WMamba.pdf",
    "documentos",
    nome_no_minio="WMamba.pdf",
    tipo="pdf",
    titulo="WMamba",
    metadata={
        "x-amz-meta-origem": "upload-usuario",
        "x-amz-meta-tipo": "documento"
    },
    salvar_txt_em="assents/WMamba.txt"
)
print(resultado)
```

### Notas sobre formatos

- `pdf` funciona bem para documentos textuais não escaneados
- `txt` é o formato mais limpo para chunking e embeddings
- `url` também é suportado pelo extrator
- se você quiser processar `.txt`, use `tipo="txt"`

## Exemplo de `main.py`

O `main.py` padrão demonstra:

- conexão com MinIO
- ingestão de documento no bucket
- processamento do documento no banco
- busca semântica

## Não versionar arquivos de dados locais

A pasta `assents/` é usada para armazenar arquivos locais e resultados de extração.
Ela não deve ir para o Git. O arquivo `.gitignore` já inclui:

```gitignore
assents/
```

## Como acessar o banco

Use o `psql` dentro do container:

```bash
docker compose exec postgres psql -U admin -d meu_banco
```

Dentro do `psql`, veja as tabelas:

```sql
\dt
```

Veja dados:

```sql
SELECT * FROM documentos LIMIT 20;
SELECT * FROM embeddings LIMIT 20;
```

Também é possível acessar do host:

```bash
psql postgresql://admin:senha123@localhost:5432/meu_banco
```

## Observações importantes

- O projeto usa `src/` como pacote Python. Portanto, as importações são feitas como `from src...`.
- O banco precisa da extensão `pgvector`. O projeto já tenta criá-la automaticamente em `src/database/models.py`.
- O `main.py` atual pode usar `ingest_documento(...)` para unificar upload + processamento.
- Preste atenção ao tipo de arquivo: não envie `.txt` como `tipo="pdf"`.

## Melhorias futuras

- adicionar tratamento de exceções ao processar documentos
- suportar mais tipos de arquivos como `docx` e `odt`
- normalizar e limpar melhor o texto antes do chunking
- expor uma API ou interface web para buscas
- suportar ingestão de arquivos diretamente do bucket sem criar temporário local

