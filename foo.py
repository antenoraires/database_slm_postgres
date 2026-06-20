import sqlalchemy

from src.config import DATABASE_URL

engine = sqlalchemy.create_engine(DATABASE_URL)
with engine.connect() as conn:
    df = conn.execute(sqlalchemy.text("select * from embeddings limit 5")).fetchall()
    print("Primeiros 5 registros da tabela 'embeddings':")
    for row in df:
        print(row)
        print("Embedding (primeiros 5 valores):", row.embedding[:5])
    conn.commit()
