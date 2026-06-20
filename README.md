# Database SLM com PostgreSQL

Uma implementação simples de um pipeline de busca semântica usando PostgreSQL com `pgvector` como banco vetorial.

## O que o projeto faz

- extrai texto de PDFs, URLs e arquivos TXT
- divide o texto em chunks
- gera embeddings usando `sentence-transformers`
- armazena documentos no PostgreSQL e embeddings no `pgvector`
- pesquisa semanticamente em conteúdos processados

## Estrutura do projeto

- `main.py` - exemplo de uso do pipeline
- `src/pipeline.py` - fluxo principal de processamento e busca
- `src/processing/` - extração e chunking de texto
- `src/embedding/` - geração de embeddings e pesquisa vetorial
- `src/database/` - modelos SQLAlchemy e inicialização do banco
- `src/config.py` - configuração do banco e modelo de embeddings
- `docker-compose.yml` - serviço PostgreSQL com `pgvector`

## Requisitos

- Python 3.12+
- Docker (recomendado para PostgreSQL)
- Dependências Python no `requirements.txt` ou `pyproject.toml`

## Instalação

1. Crie e ative o ambiente virtual

```bash
cd /Users/aires/Downloads/projetos/database_slm_postgres
uv init
uv venv
source .venv/bin/activate
uv sync
```

2. Instale as dependências

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

## Uso

Execute o script principal:

```bash
python main.py
```

Ou, se você usa `uv`:

```bash
uv run python main.py
```

O `main.py`:

- instancia o `Pipeline`
- processa documentos
- realiza uma busca semântica

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
- O banco precisa da extensão `pgvector`. O projeto já tenta criá-la automaticamente no `src/database/models.py`.
- Mais arquivos e conteúdo relevantes melhoram a qualidade das respostas da busca semântica.

## Melhorias futuras

- adicionar tratamento de exceções ao processar documentos
- suportar mais tipos de arquivos
- normalizar e limpar melhor o texto antes do chunking
- expor uma API ou interface web para buscas

