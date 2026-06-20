import PyPDF2
import requests
from bs4 import BeautifulSoup
from pathlib import Path

class TextExtractor:
    @staticmethod
    def from_pdf(caminho: str) -> str:
        texto = ""
        with open(caminho, 'rb') as f:
            leitor = PyPDF2.PdfReader(f)
            for pagina in leitor.pages:
                texto += pagina.extract_text() + "\n"
        return texto
    
    @staticmethod
    def from_url(url: str) -> str:
        resposta = requests.get(url, timeout=30)
        sopa = BeautifulSoup(resposta.content, 'html.parser')
        # Remove scripts e estilos
        for tag in sopa(['script', 'style']):
            tag.decompose()
        return sopa.get_text(separator='\n', strip=True)
    
    @staticmethod
    def from_txt(caminho: str) -> str:
        return Path(caminho).read_text(encoding='utf-8')