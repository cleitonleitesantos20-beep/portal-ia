from database import SessionLocal, criar_banco
import models

# 1. Garante que as tabelas existam
criar_banco()
db = SessionLocal()

# 2. Limpa produtos antigos para aplicar a nova estrutura limpa
try:
    db.query(models.Produto).delete()
    db.commit()
except:
    db.rollback()

produtos = [
    # --- SEÇÃO 1: AUXILIADORES (Tipo: web_bot) ---
    models.Produto(
        nome="Nexus Mines Bot",
        slug="mines",
        descricao="Algoritmo de IA para análise de padrões em tempo real.",
        preco="", # Deixamos vazio conforme solicitado
        tipo="web_bot",
        categoria="Auxiliador",
        imagem_url="https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=500",
        link_venda="https://COLOQUE-SEU-LINK-AQUI.com"
    ),
    models.Produto(
        nome="Blackjack Master IA",
        slug="blackjack",
        descricao="Análise probabilística avançada para tomada de decisão.",
        preco="",
        tipo="web_bot",
        categoria="Auxiliador",
        imagem_url="https://images.unsplash.com/photo-1511193311914-0346f16bee90?w=500",
        link_venda="https://COLOQUE-SEU-LINK-AQUI.com"
    ),

    # --- SEÇÃO 2: TRADES & SINAIS (Tipo: trade_bot) ---
    models.Produto(
        nome="Sniper Crypto Win",
        slug="trade-cripto",
        descricao="Automação estratégica via API para o mercado de criptoativos.",
        preco="",
        tipo="trade_bot",
        categoria="Trade",
        imagem_url="https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=500",
        link_venda="https://COLOQUE-SEU-LINK-AQUI.com"
    ),

    # --- SEÇÃO 3: E-BOOKS (Tipo: ebook) ---
    models.Produto(
        nome="Manual do Lucro com IA",
        slug="ebook-riqueza",
        descricao="Guia estratégico sobre automação e geração de renda.",
        preco="",
        tipo="ebook",
        categoria="Educação",
        imagem_url="https://images.unsplash.com/photo-1589998059171-988d887df646?w=500",
        link_venda="https://COLOQUE-SEU-LINK-AQUI.com"
    ),

    # --- SEÇÃO 4: ITENS (Antigo Parceiros) (Tipo: infoproduto) ---
    models.Produto(
        nome="Curso Dominando Algoritmos",
        slug="curso-hotmart",
        descricao="Treinamento completo focado em lógica e IA aplicada.",
        preco="",
        tipo="infoproduto",
        categoria="Itens",
        imagem_url="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=500",
        link_venda="https://hotmart.com/SEU-LINK-AQUI"
    ),
    models.Produto(
        nome="Setup Gamer IA",
        slug="setup-amazon",
        descricao="Equipamentos recomendados para alta performance.",
        preco="",
        tipo="infoproduto",
        categoria="Itens",
        imagem_url="https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500",
        link_venda="https://amazon.com.br/SEU-LINK-AQUI"
    )
]

# 3. Adicionando os produtos ao banco com segurança
try:
    db.add_all(produtos)
    db.commit()
    print("🚀 MARKETPLACE INTELIGENTE/A: Banco atualizado e limpo!")
except Exception as e:
    db.rollback()
    print(f"❌ Erro ao atualizar o banco: {e}")
finally:
    db.close()
