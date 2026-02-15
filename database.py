from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os
# Isso garante que ele ache o banco na pasta atual do servidor
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "portal.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

# O arquivo do banco será criado automaticamente na pasta do projeto
SQLALCHEMY_DATABASE_URL = "sqlite:///./portal.db"

# O engine é o motor que gerencia a conexão
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} # Necessário apenas para SQLite
)

# Cria a fábrica de sessões para conversar com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para criar as tabelas
def criar_banco():
    Base.metadata.create_all(bind=engine)