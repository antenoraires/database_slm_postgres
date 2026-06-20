from src.pipeline import Pipeline

p = Pipeline()

# Processa documentos
#p.processar_documento("assents/rsl_antenor.pdf", tipo="pdf")
#p.processar_documento("https://www.eftsure.com/blog/cyber-crime/these-7-deepfake-ceo-scams-prove-that-no-business-is-safe/", tipo="url")

# Busca inteligente
resultados = p.buscar("Qual a universidade com mais destaque nos estudos sobre deepfake?", top_k=3)

for r in resultados:
    print(f"Score: {r['similaridade']:.3f}")
    print(f"Trecho: {r['texto'][:300]}...\n")