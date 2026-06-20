from pytest import fixture
from src.database.models import SessionLocal, Documento, Embedding


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

