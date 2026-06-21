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

    @staticmethod
    def save_text(texto: str, destino: str) -> str:
        """Salva texto em arquivo .txt e retorna o caminho gerado."""
        Path(destino).write_text(texto, encoding='utf-8')
        return destino

    def to_txt(self, fonte: str, tipo: str = 'pdf', destino: str | None = None) -> str:
        """Extrai texto de uma fonte e opcionalmente salva em um arquivo .txt."""
        if tipo == 'pdf':
            texto = self.from_pdf(fonte)
        elif tipo == 'url':
            texto = self.from_url(fonte)
        elif tipo == 'txt':
            texto = self.from_txt(fonte)
        else:
            raise ValueError(f"Tipo '{tipo}' não suportado para conversão para txt")

        if destino:
            self.save_text(texto, destino)
        return texto

    def pdf_to_txt(self, caminho_pdf: str, destino_txt: str) -> str:
        """Converte PDF para texto e salva em destino_txt."""
        texto = self.from_pdf(caminho_pdf)
        return self.save_text(texto, destino_txt)

    def url_to_txt(self, url: str, destino_txt: str) -> str:
        """Converte o conteúdo de uma URL para texto e salva em destino_txt."""
        texto = self.from_url(url)
        return self.save_text(texto, destino_txt)

    def any_to_txt(self, fonte: str, tipo: str, destino_txt: str) -> str:
        """Converte qualquer fonte suportada para texto e salva em destino_txt."""
        return self.to_txt(fonte, tipo=tipo, destino=destino_txt)
