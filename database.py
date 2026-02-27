import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# 1. Localiza a pasta atual do projeto para salvar o banco local
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "portal.db")

# 2. Configuração da URL do Banco de Dados
# Se você colocar uma URL do PostgreSQL no Render, ele usará ela. 
# Caso contrário, usará o SQLite local (portal.db).
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

# Pequeno ajuste para compatibilidade com versões novas do PostgreSQL no Render
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Criação do Engine (Motor)
# O "check_same_thread" é um ajuste obrigatório apenas para o SQLite
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args=connect_args
)

# 4. Fábrica de sessões (onde as transações acontecem)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Função para criar as tabelas no banco de dados
def criar_banco():
    """
    Lê o arquivo models.py e cria as tabelas se elas não existirem.
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Estrutura do banco de dados verificada/criada com sucesso.")
