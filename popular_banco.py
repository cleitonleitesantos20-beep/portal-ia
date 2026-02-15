from database import SessionLocal, criar_banco
import models

# Garante que o banco e as tabelas existam
criar_banco()

def inserir_dados():
    db = SessionLocal()
    
    # Limpa o banco antes de inserir (opcional, para não duplicar no teste)
    db.query(models.Noticia).delete()

    noticias_teste = [
        models.Noticia(
            titulo="Tesla Optimus Gen 3: O robô que já ajuda em tarefas domésticas",
            categoria="Robótica Doméstica",
            conteudo="O novo modelo da Tesla impressionou o mercado com sua capacidade de dobrar roupas e organizar cozinhas com precisão milimétrica. Especialistas dizem que 2026 será o ano da adoção em massa...",
            imagem_url="https://images.unsplash.com/photo-1546776310-eef45dd6d63c?auto=format&fit=crop&q=80&w=400"
        ),
        models.Noticia(
            titulo="Estratégia Nexus: Como o robô de trade atingiu 85% de acerto",
            categoria="Finanças IA",
            conteudo="Utilizando redes neurais profundas, o sistema Nexus Alpha conseguiu prever movimentações de baleias no mercado de criptoativos antes mesmo da execução das ordens...",
            imagem_url="https://images.unsplash.com/photo-1644029835102-019946857640?auto=format&fit=crop&q=80&w=400"
        ),
        models.Noticia(
            titulo="GPT-5 e o fim das interfaces tradicionais",
            categoria="IA Generativa",
            conteudo="A nova atualização da OpenAI promete uma integração neural que dispensa o uso de teclados. O sistema agora entende intenções antes mesmo de serem verbalizadas...",
            imagem_url="https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=400"
        )
    ]

    try:
        db.add_all(noticias_teste)
        db.commit()
        print("✅ Portal atualizado com imagens profissionais!")
    except Exception as e:
        print(f"❌ Erro ao inserir: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    inserir_dados()