from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Define a base para a criação das tabelas
Base = declarative_base()

class Noticia(Base):
    __tablename__ = "noticias"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200))
    categoria = Column(String(50)) # Ex: Robótica, IA, Estratégia
    conteudo = Column(Text)
    imagem_url = Column(String(500)) 
    data_criacao = Column(DateTime, default=datetime.utcnow)

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))
    
    # O 'slug' é essencial para as rotas de acesso (ex: /app/acesso/mines)
    slug = Column(String(100), unique=True, index=True) 
    
    descricao = Column(Text)
    
    # Deixamos o preço como opcional (nullable=True) 
    # Já que no seu novo layout os preços foram removidos visualmente
    preco = Column(String(50), nullable=True)  
    
    # tipo: 'web_bot', 'trade_bot', 'ebook', 'infoproduto'
    # Importante: mantenha 'infoproduto' para a seção que agora chamamos de 'ITENS'
    tipo = Column(String(50))   
    
    # categoria: 'Auxiliador', 'Trade', 'Educação', 'Itens'
    categoria = Column(String(50)) 
    
    imagem_url = Column(String(500))
    
    # Link de destino (Checkout, Hotmart, Shopee, Amazon, etc.)
    link_venda = Column(String(500)) 
    
    # arquivo_url: Para casos onde você ainda queira fornecer um download direto
    arquivo_url = Column(String(500), nullable=True)
