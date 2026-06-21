import os
from typing import Sequence

from transformers import pipeline, set_seed

RAG_MODEL = os.getenv("RAG_MODEL", "google/flan-t5-small")
RAG_MAX_LENGTH = int(os.getenv("RAG_MAX_LENGTH", "256"))
RAG_TEMPERATURE = float(os.getenv("RAG_TEMPERATURE", "0.2"))

generator = pipeline("text-generation", model=RAG_MODEL)
set_seed(42)


def build_rag_prompt(query: str, chunks: Sequence[dict], max_chunks: int = 3) -> str:
    trecho_textos = []
    for i, chunk in enumerate(chunks[:max_chunks]):
        texto = chunk.get("texto", "")
        documento_id = chunk.get("documento_id")
        trecho_textos.append(f"Trecho {i+1} (doc {documento_id}):\n{texto}")

    context = "\n\n---\n\n".join(trecho_textos)
    return (
        "Use os trechos abaixo como contexto para responder a pergunta. "
        "Seja direto, cite as fontes pelo ID do documento e não invente informações.\n\n"
        f"{context}\n\n"
        f"Pergunta: {query}\n"
        "Resposta:"
    )


def gerar_resposta(query: str, resultados: Sequence[dict], top_k: int = 5) -> str | None:
    if not resultados:
        return None

    prompt = build_rag_prompt(query, resultados, max_chunks=min(top_k, 3))
    resposta = generator(
        prompt,
        max_length=RAG_MAX_LENGTH,
        do_sample=True,
        temperature=RAG_TEMPERATURE,
        num_return_sequences=1,
    )
    return resposta[0]["generated_text"].strip()


def is_rag_available() -> bool:
    return True
