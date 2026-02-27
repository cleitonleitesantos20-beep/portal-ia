from database import SessionLocal, criar_banco
import models

# 1. Garante que as tabelas existam seguindo o models.py revisado
criar_banco()

def popular():
    db = SessionLocal()
    
    try:
        # Limpamos as duas tabelas para não duplicar dados durante os testes
        db.query(models.Noticia).delete()
        db.query(models.Produto).delete()
        print("🧹 Banco de dados limpo com sucesso.")

        # --- SEÇÃO 1: NOTÍCIAS (PORTAL) ---
        noticias = [
            models.Noticia(
                titulo="Tesla Optimus Gen 3: O robô que já ajuda em tarefas domésticas",
                categoria="Robótica",
                conteudo="O novo modelo da Tesla impressionou o mercado com sua capacidade de organização. Especialistas dizem que 2026 será o ano da adoção em massa.",
                imagem_url="https://images.unsplash.com/photo-1546776310-eef45dd6d63c?w=500"
            ),
            models.Noticia(
                titulo="GPT-5 e o futuro da Inteligência Artificial em 2026",
                categoria="IA",
                conteudo="A nova atualização promete uma integração neural fluida, mudando como interagimos com a tecnologia no dia a dia.",
                imagem_url="https://images.unsplash.com/photo-1677442136019-21780ecad995?w=500"
            )
        ]

        # --- SEÇÃO 2: PRODUTOS (MARKETPLACE INTELIGENTE/A) ---
        # Lembre-se: Preços removidos e slugs batendo com suas rotas de acesso
        produtos = [
            models.Produto(
                nome="Nexus Mines Bot",
                slug="mines",
                descricao="Algoritmo de IA para análise de padrões. Focado em alta precisão.",
                tipo="web_bot",
                categoria="Auxiliador",
                imagem_url="https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=500",
                link_venda="https://seu-link-de-venda.com/mines"
            ),
            models.Produto(
                nome="Sniper Crypto Pro",
                slug="trade-cripto",
                descricao="Automação estratégica para o mercado de criptoativos.",
                tipo="trade_bot",
                categoria="Trade",
                imagem_url="https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=500",
                link_venda="https://seu-link-de-venda.com/crypto"
            ),
            models.Produto(
                nome="E-book: Mestre da Automação",
                slug="ebook-ia",
                descricao="Guia prático para dominar ferramentas de IA em 2026.",
                tipo="ebook",
                categoria="Educação",
                imagem_url="https://images.unsplash.com/photo-1589998059171-988d887df646?w=500",
                link_venda="https://seu-link-de-venda.com/ebook"
            ),
            models.Produto(
                nome="Curso Algoritmos Avançados",
                slug="curso-itens",
                descricao="Treinamento completo para desenvolvedores e entusiastas.",
                # Usamos infoproduto para cair na seção "ITENS" do seu HTML
                tipo="infoproduto", 
                categoria="Itens",
                imagem_url="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=500",
                link_venda="https://hotmart.com/seu-link"
            )
        ]

        # Adicionamos tudo ao banco
        db.add_all(noticias)
        db.add_all(produtos)
        db.commit()
        print("🚀 PORTAL & MARKETPLACE: Dados inseridos com sucesso!")

    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao popular banco: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    popular()
