from database import SessionLocal, criar_banco
import models

# 1. Garante que as tabelas existam
criar_banco()
db = SessionLocal()

# 2. Limpa produtos antigos para aplicar a nova estrutura de prateleiras
db.query(models.Produto).delete()

produtos = [
    # --- SEÇÃO 1: AUXILIADORES (Tipo: web_bot) ---
    models.Produto(
        nome="Nexus Mines Bot",
        slug="mines",
        descricao="Algoritmo de IA para padrões de minas.",
        preco="R$ 49,90 / mês",
        tipo="web_bot",
        categoria="Auxiliador",
        imagem_url="https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=500",
        link_venda="https://seu-checkout.com/mines"
    ),
    models.Produto(
        nome="Blackjack Master IA",
        slug="blackjack",
        descricao="Análise probabilística em tempo real.",
        preco="R$ 59,90 / mês",
        tipo="web_bot",
        categoria="Auxiliador",
        imagem_url="https://images.unsplash.com/photo-1511193311914-0346f16bee90?w=500",
        link_venda="https://seu-checkout.com/blackjack"
    ),

    # --- SEÇÃO 2: TRADES (Tipo: trade_bot) ---
    models.Produto(
        nome="Sniper Crypto Win",
        slug="trade-cripto",
        descricao="Automação de scalp via API.",
        preco="R$ 297,00 (Vitalício)",
        tipo="trade_bot",
        categoria="Trade",
        imagem_url="https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=500",
        link_venda="https://seu-checkout.com/cripto-bot"
    ),

    # --- SEÇÃO 3: E-BOOKS (Tipo: ebook) ---
    models.Produto(
        nome="Manual do Lucro com IA",
        slug="ebook-riqueza",
        descricao="Guia de automação 2026.",
        preco="R$ 37,00",
        tipo="ebook",
        categoria="Educação",
        imagem_url="https://images.unsplash.com/photo-1589998059171-988d887df646?w=500",
        link_venda="https://seu-checkout.com/ebook-ia"
    ),

    # --- SEÇÃO 4: INFOPRODUTOS (Hotmart, Amazon, Shopee) (Tipo: infoproduto) ---
    models.Produto(
        nome="Curso Dominando Algoritmos",
        slug="curso-hotmart",
        descricao="Hotmart", # Usamos a descrição para indicar a loja no novo layout
        preco="R$ 197,00",
        tipo="infoproduto",
        categoria="Parceiro",
        imagem_url="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=500",
        link_venda="https://hotmart.com/seu-link"
    ),
    models.Produto(
        nome="Setup Gamer IA (Promoção)",
        slug="setup-amazon",
        descricao="Amazon",
        preco="Ver Preço",
        tipo="infoproduto",
        categoria="Parceiro",
        imagem_url="https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500",
        link_venda="https://amazon.com.br/seu-link"
    ),

    # --- SEÇÃO 5: OUTROS (Em Desenvolvimento) (Tipo: afiliado) ---
    models.Produto(
        nome="Robô de Informação",
        slug="robo-info",
        descricao="EM DESENVOLVIMENTO",
        preco="BREVE",
        tipo="afiliado",
        categoria="Futuro",
        imagem_url="",
        link_venda="#"
    )
]

db.add_all(produtos)
db.commit()
print("🚀 Banco de dados atualizado com as novas fileiras e Infoprodutos!")
db.close()