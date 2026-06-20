import sqlalchemy
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:senha123@localhost:5432/meu_banco"
)

engine = sqlalchemy.create_engine(DATABASE_URL)
