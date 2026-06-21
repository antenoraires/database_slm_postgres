import PyPDF2
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
import unicodedata

class TextExtractor:
    @staticmethod
    def from_pdf(caminho: str) -> str:
        texto = ""
        with open(caminho, 'rb') as f:
            leitor = PyPDF2.PdfReader(f)
            for pagina in leitor.pages:
                texto += pagina.extract_text() + "\n"
        return TextExtractor.clean_text(texto)
    
    @staticmethod
    def from_url(url: str) -> str:
        resposta = requests.get(url, timeout=30)
        sopa = BeautifulSoup(resposta.content, 'html.parser')
        # Remove scripts e estilos
        for tag in sopa(['script', 'style']):
            tag.decompose()
        texto = sopa.get_text(separator='\n', strip=True)
        return TextExtractor.clean_text(texto)
    
    @staticmethod
    def from_txt(caminho: str) -> str:
        texto = Path(caminho).read_text(encoding='utf-8')
        return TextExtractor.clean_text(texto)

    @staticmethod
    def normalize_text(texto: str) -> str:
        texto = texto.replace('\r\n', '\n').replace('\r', '\n')
        texto = texto.replace('\t', ' ')
        texto = unicodedata.normalize('NFKC', texto)
        texto = re.sub(r'(\w+)-\n(\w+)', r'\1\2', texto)
        texto = re.sub(r'([a-zà-úÀ-Ú0-9])\n([a-zà-ú])', r'\1 \2', texto)
        texto = re.sub(r'(?im)^(?:p(?:á|a)gina|page|pg|p)\s*\d+\s*(?:de|of)\s*\d+\s*$', '', texto)
        texto = re.sub(r'(?m)^\s*\d+\s*/\s*\d+\s*$', '', texto)
        texto = re.sub(r'[ \t]+', ' ', texto)
        texto = re.sub(r'\n{3,}', '\n\n', texto)
        texto = texto.strip()
        return texto

    @staticmethod
    def remove_control_characters(texto: str) -> str:
        return ''.join(
            ch for ch in texto
            if ch == '\n' or unicodedata.category(ch)[0] != 'C'
        )

    @staticmethod
    def clean_text(texto: str) -> str:
        texto = TextExtractor.remove_control_characters(texto)
        texto = TextExtractor.normalize_text(texto)
        return texto

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
