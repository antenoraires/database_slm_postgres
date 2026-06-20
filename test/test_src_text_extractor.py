from src.processing.text_extractor import TextExtractor

from pytest import fixture

@fixture(scope="module")
def test_text_extractor_from_txt(tmp_path):
    arquivo = tmp_path / "teste.txt"
    arquivo.write_text("conteúdo de teste", encoding="utf-8")

    texto = TextExtractor.from_txt(str(arquivo))

    assert texto == "conteúdo de teste"


def test_text_extractor_from_url(monkeypatch):
    html = "<html><head><style>body{}</style><script>alert(1)</script></head><body>texto <b>importante</b></body></html>"

    class FakeResponse:
        content = html.encode("utf-8")

    monkeypatch.setattr("src.processing.text_extractor.requests.get", lambda url, timeout: FakeResponse())

    texto = TextExtractor.from_url("https://example.com")

    assert "texto importante" in texto
    assert "script" not in texto
    assert "style" not in texto


def test_text_extractor_from_pdf(monkeypatch):
    class FakePage:
        def __init__(self, text):
            self._text = text

        def extract_text(self):
            return self._text

    class FakePdfReader:
        def __init__(self, _):
            self.pages = [FakePage("pagina 1"), FakePage("pagina 2")]

    monkeypatch.setattr("src.processing.text_extractor.PyPDF2.PdfReader", FakePdfReader)

    texto = TextExtractor.from_pdf("arquivo.pdf")

    assert "pagina 1" in texto
    assert "pagina 2" in texto