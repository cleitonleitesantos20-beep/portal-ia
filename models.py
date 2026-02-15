from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Define a base para a criação das tabelas
Base = declarative_base()

class Noticia(Base):
    __tablename__ = "noticias"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200))
    categoria = Column(String(50)) # Ex: Robótica, IA
    conteudo = Column(Text)
    imagem_url = Column(String(500)) # Link da imagem da notícia
    data_criacao = Column(DateTime, default=datetime.utcnow)

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))
    
    # O 'slug' servirá para criar a URL individual (ex: /app/acesso/mines)
    slug = Column(String(100), unique=True, index=True) 
    
    descricao = Column(Text)
    preco = Column(String(50))  # Ex: "R$ 97,00 / mês"
    
    # tipo: 'web_bot' (SaaS), 'trade_bot' (PC), 'ebook' (Download), 'afiliado'
    tipo = Column(String(50))   
    
    # categoria: 'Cripto', 'Forex', 'Cassino', 'Ebook', 'Info'
    categoria = Column(String(50)) 
    
    imagem_url = Column(String(500))
    link_venda = Column(String(500)) # Link do checkout
    
    # arquivo_url: Link direto para o PDF ou Instalador EXE
    arquivo_url = Column(String(500), nullable=True)