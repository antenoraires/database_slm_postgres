from src.embedding.vector_store import VectorStore
from conftest import DummyGenerator

from pytest import fixture

@fixture(scope="module")
def test_vector_store_inserir_chunks(monkeypatch):
    events = []

    class DummySession:
        def __init__(self):
            self.added = []
        def add(self, obj):
            self.added.append(obj)
        def commit(self):
            events.append("commit")
        def close(self):
            events.append("close")

    def fake_sessionlocal():
        return DummySession()

    store = VectorStore()
    monkeypatch.setattr(store, "generator", DummyGenerator())
    monkeypatch.setattr("src.embedding.vector_store.SessionLocal", fake_sessionlocal)

    store.inserir_chunks(1, ["chunk1", "chunk2"])

    assert events == ["commit", "close"]


def test_vector_store_buscar_similar(monkeypatch):
    rows = [
        type("R", (), {"chunk_texto": "texto 1", "documento_id": 1, "embedding": [0.1]*384}),
        type("R", (), {"chunk_texto": "texto 2", "documento_id": 1, "embedding": [0.1]*384})
    ]

    class FakeQuery:
        def order_by(self, _):
            return self
        def limit(self, _):
            return self
        def all(self):
            return rows

    class DummySession:
        def query(self, _):
            return FakeQuery()
        def close(self):
            pass

    store = VectorStore()
    monkeypatch.setattr(store, "generator", DummyGenerator())
    monkeypatch.setattr("src.embedding.vector_store.SessionLocal", lambda: DummySession())

    resultados = store.buscar_similar("teste", top_k=2)

    assert len(resultados) == 2
    assert all("similaridade" in r for r in resultados)