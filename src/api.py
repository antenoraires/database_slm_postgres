from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from src.pipeline import Pipeline

app = FastAPI()

pipeline = Pipeline()

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    texto: str
    documento_id: int
    similaridade: float

class SearchResponse(BaseModel):
    query: str
    top_k: int
    resultados: list[SearchResult]

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    resultados = pipeline.buscar(request.query, top_k=request.top_k)
    return SearchResponse(
        query=request.query,
        top_k=request.top_k,
        resultados=[SearchResult(**r) for r in resultados]
    )

@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(
        """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Busca Semântica</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                input, button, textarea { font-size: 1rem; }
                textarea { width: 100%; height: 120px; margin-top: 8px; }
                .result { border: 1px solid #ddd; padding: 12px; margin-top: 12px; border-radius: 6px; }
                .score { color: #333; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>Busca Semântica</h1>
            <p>Digite uma pergunta e veja os resultados do `p.buscar(...)`.</p>
            <label for="query">Pergunta</label>
            <textarea id="query" placeholder="Ex: rostos gerados por GAN?"></textarea>
            <br />
            <label for="top_k">Top K</label>
            <input type="number" id="top_k" value="5" min="1" max="20" />
            <br /><br />
            <button id="searchButton">Buscar</button>
            <div id="status" style="margin-top: 16px; color: #555;"></div>
            <div id="results"></div>
            <script>
                const button = document.getElementById('searchButton');
                const queryField = document.getElementById('query');
                const topKField = document.getElementById('top_k');
                const resultsDiv = document.getElementById('results');
                const statusDiv = document.getElementById('status');

                button.addEventListener('click', async () => {
                    const query = queryField.value.trim();
                    const top_k = Number(topKField.value) || 5;
                    if (!query) {
                        statusDiv.textContent = 'Digite uma pergunta antes de buscar.';
                        return;
                    }
                    statusDiv.textContent = 'Buscando...';
                    resultsDiv.innerHTML = '';

                    try {
                        const response = await fetch('/search', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ query, top_k })
                        });
                        const data = await response.json();
                        if (!response.ok) {
                            statusDiv.textContent = 'Erro ao buscar: ' + (data.detail || response.statusText);
                            return;
                        }
                        statusDiv.textContent = `Resultados para: "${data.query}"`;
                        if (!data.resultados.length) {
                            resultsDiv.innerHTML = '<p>Nenhum resultado encontrado.</p>';
                            return;
                        }
                        data.resultados.forEach((item, index) => {
                            const div = document.createElement('div');
                            div.className = 'result';
                            div.innerHTML = `
                                <div class="score">#${index + 1} - similaridade: ${item.similaridade.toFixed(4)}</div>
                                <div><strong>Documento ID:</strong> ${item.documento_id}</div>
                                <div><strong>Trecho:</strong> <pre style="white-space: pre-wrap;">${item.texto}</pre></div>
                            `;
                            resultsDiv.appendChild(div);
                        });
                    } catch (error) {
                        statusDiv.textContent = 'Erro na requisição: ' + error.message;
                    }
                });
            </script>
        </body>
        </html>
        """
    )
