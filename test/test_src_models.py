import io
import numpy as np
import pytest

from pytest import fixture
from src.pipeline import Pipeline
from src.embedding.vector_store import VectorStore
from src.processing.chunker import TextChunker
from src.database.models import SessionLocal, Documento, Embedding
from conftest import  DummyGenerator, DummyEmbedding


@fixture(scope="module")
def test_db_session():
    """Fixture para criar uma sessão de teste no banco"""
    session = SessionLocal()
    yield session
    session.close()

def test_documento_model(test_db_session):
    """Teste básico para o modelo Documento"""
    doc = Documento(titulo="Teste", fonte="test.txt", texto_completo="Texto de teste")
    test_db_session.add(doc)
    test_db_session.commit()
    
    assert doc.id is not None
    assert doc.titulo == "Teste"
    assert doc.fonte == "test.txt"
    assert doc.texto_completo == "Texto de teste"

def test_embedding_model(test_db_session):
    """Teste básico para o modelo Embedding"""
    emb = Embedding(documento_id=1, chunk_texto="Chunk de teste", embedding=[0.1]*384, posicao_chunk=0)
    test_db_session.add(emb)
    test_db_session.commit()
    
    assert emb.id is not None
    assert emb.documento_id == 1
    assert emb.chunk_texto == "Chunk de teste"
    assert len(emb.embedding) == 384
    assert emb.posicao_chunk == 0

###
###

def test_pipeline_buscar_calls_vector_store(monkeypatch):
    pipeline = Pipeline()
    monkeypatch.setattr(pipeline, "vector_store", type("VS", (), {"buscar_similar": lambda self, pergunta, top_k=5: [{"texto": "a", "similaridade": 0.9}]} )())

    resultados = pipeline.buscar("pergunta")
    assert resultados == [{"texto": "a", "similaridade": 0.9}]


def test_pipeline_processar_documento(monkeypatch):
    pipeline = Pipeline()
    monkeypatch.setattr(pipeline, 'extractor', type('E', (), {
        'from_pdf': staticmethod(lambda caminho: 'texto pdf teste'),
        'from_url': staticmethod(lambda url: 'texto url teste'),
        'from_txt': staticmethod(lambda caminho: 'texto txt teste')
    })())
    monkeypatch.setattr(pipeline, 'chunker', TextChunker(chunk_size=3, overlap=1))
    dummy_store = VectorStore()
    monkeypatch.setattr(dummy_store, 'inserir_chunks', lambda documento_id, chunks: None)
    monkeypatch.setattr(pipeline, 'vector_store', dummy_store)

    class FakeSession:
        def add(self, obj):
            pass
        def commit(self):
            pass
        def close(self):
            pass

    monkeypatch.setattr("src.pipeline.SessionLocal", lambda: FakeSession())

    resultado = pipeline.processar_documento('arquivo.txt', tipo='txt', titulo='Teste')
    assert isinstance(resultado, int)

    with pytest.raises(ValueError):
        pipeline.processar_documento('arquivo.txt', tipo='docx')


@pytest.fixture
def dummy_vector_store(monkeypatch):
    store = VectorStore()
    monkeypatch.setattr(store, 'generator', DummyGenerator())
    return store


def test_vector_store_cosine_similarity(dummy_vector_store):
    vector_a = np.array([1.0, 0.0])
    vector_b = np.array([0.0, 1.0])

    similarity = dummy_vector_store._cosine_similarity(vector_a, vector_b)
    assert similarity == pytest.approx(0.0)

    similarity_same = dummy_vector_store._cosine_similarity(vector_a, vector_a)
    assert similarity_same == pytest.approx(1.0)


def test_vector_store_zero_vector(dummy_vector_store):
    vector_a = np.array([0.0, 0.0])
    vector_b = np.array([1.0, 0.0])

    assert dummy_vector_store._cosine_similarity(vector_a, vector_b) == 0.0


@pytest.mark.skip(reason="requires actual DB and pgvector query support")
def test_vector_store_search(dummy_vector_store, test_db_session, monkeypatch):
    # Este teste é apenas ilustrativo; a consulta real depende de pgvector no DB.
    pass


def test_pipeline_processar_documento(monkeypatch):
    pipeline = Pipeline()
    monkeypatch.setattr(pipeline, 'extractor', type('E', (), {
        'from_pdf': staticmethod(lambda caminho: 'texto pdf teste'),
        'from_url': staticmethod(lambda url: 'texto url teste'),
        'from_txt': staticmethod(lambda caminho: 'texto txt teste')
    })())
    monkeypatch.setattr(pipeline, 'chunker', TextChunker(chunk_size=3, overlap=1))
    dummy_store = VectorStore()
    monkeypatch.setattr(dummy_store, 'inserir_chunks', lambda documento_id, chunks: None)
    monkeypatch.setattr(pipeline, 'vector_store', dummy_store)

    resultado = pipeline.processar_documento('arquivo.txt', tipo='txt', titulo='Teste')
    assert isinstance(resultado, int)

    with pytest.raises(ValueError):
        pipeline.processar_documento('arquivo.txt', tipo='docx')

