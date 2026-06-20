from src.processing.chunker import TextChunker

from pytest import fixture

@fixture(scope="module")
def test_text_chunker():
    chunker = TextChunker(chunk_size=5, overlap=2)
    texto = "este é um texto de teste para chunker"

    chunks = chunker.chunk(texto)

    assert len(chunks) == 4
    assert chunks[0] == "este é um texto de"
    assert chunks[1] == "texto de teste para"
    assert chunks[2] == "teste para chunker"
    assert chunks[3] == "chunker"