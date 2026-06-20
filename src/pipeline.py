from src.processing.text_extractor import TextExtractor
from src.processing.chunker import TextChunker
from src.database.models import Documento, SessionLocal
from src.embedding.vector_store import VectorStore
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

class Pipeline:
    def __init__(self):
        self.extractor = TextExtractor()
        self.chunker = TextChunker(CHUNK_SIZE, CHUNK_OVERLAP)
        self.vector_store = VectorStore()
    
    def processar_documento(self, fonte: str, tipo: str = "pdf", titulo: str = None):
        """
        Fluxo completo: extrair → salvar → chunkar → embeddar
        """
        # 1. Extrair texto
        if tipo == "pdf":
            texto = self.extractor.from_pdf(fonte)
        elif tipo == "url":
            texto = self.extractor.from_url(fonte)
        elif tipo == "txt":
            texto = self.extractor.from_txt(fonte)
        else:
            raise ValueError(f"Tipo '{tipo}' não suportado")
        
        # 2. Salvar no banco relacional
        session = SessionLocal()
        doc = Documento(
            titulo=titulo or fonte,
            fonte=fonte,
            texto_completo=texto
        )
        session.add(doc)
        session.commit()
        doc_id = doc.id
        session.close()
        
        # 3. Chunkar
        chunks = self.chunker.chunk(texto)
        
        # 4. Gerar embeddings e salvar no vetorial
        self.vector_store.inserir_chunks(doc_id, chunks)
        
        print(f"✅ Documento '{titulo}' processado!")
        print(f"   - ID: {doc_id}")
        print(f"   - Chunks: {len(chunks)}")
        
        return doc_id
    
    def buscar(self, pergunta: str, top_k: int = 5):
        """Busca semântica nos documentos processados"""
        return self.vector_store.buscar_similar(pergunta, top_k)
