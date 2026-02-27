from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import models
from database import SessionLocal, criar_banco
import re  # [NOVO] Importado para gerar URLs amigáveis (slugs)

app = FastAPI()

# 1. Inicializa o banco (Garante que as tabelas existam ao iniciar)
criar_banco()

# 2. Configurações de arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 3. Dependência para abrir e fechar a conexão com o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROTAS PÚBLICAS ---

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    noticias = db.query(models.Noticia).order_by(models.Noticia.id.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "noticias": noticias})

@app.get("/post/{post_id}")
async def pagina_noticia(request: Request, post_id: int, db: Session = Depends(get_db)):
    noticia = db.query(models.Noticia).filter(models.Noticia.id == post_id).first()
    if not noticia:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    return templates.TemplateResponse("post.html", {"request": request, "noticia": noticia})

@app.get("/produtos")
async def pagina_produtos(request: Request, db: Session = Depends(get_db)):
    lista_db = db.query(models.Produto).all()
    return templates.TemplateResponse("produtos.html", {"request": request, "produtos": lista_db})

# --- SISTEMA VIP ---

@app.get("/app/acesso/{robo_slug}")
async def login_robo_page(request: Request, robo_slug: str):
    return templates.TemplateResponse("robo_vip.html", {"request": request, "slug": robo_slug})

@app.post("/app/validar/{robo_slug}")
async def validar_acesso(request: Request, robo_slug: str, chave: str = Form(...)):
    CHAVE_ATUAL = "VIP2026_FEV" 
    if chave == CHAVE_ATUAL:
        return templates.TemplateResponse(f"paineis/{robo_slug}.html", {"request": request})
    else:
        return templates.TemplateResponse("robo_vip.html", {
            "request": request, "slug": robo_slug, "erro": "❌ Chave inválida ou expirada."
        })

# --- ADMINISTRAÇÃO (POSTAR NOTÍCIAS E PRODUTOS) ---

@app.get("/admin")
async def pagina_admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.post("/admin/postar")
async def salvar_noticia(
    titulo: str = Form(...), 
    categoria: str = Form(...), 
    conteudo: str = Form(...), 
    imagem_url: str = Form(...),
    db: Session = Depends(get_db)
):
    nova_noticia = models.Noticia(
        titulo=titulo, categoria=categoria, conteudo=conteudo, imagem_url=imagem_url
    )
    db.add(nova_noticia)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

# [NOVA ROTA] Salva o Produto vindo do Admin
@app.post("/admin/cadastrar_produto")
async def salvar_produto(
    nome: str = Form(...),
    tipo: str = Form(...),
    categoria_txt: str = Form(...), # Recebe o texto da categoria do Admin
    preco: str = Form(None),         # Preço opcional
    imagem_url: str = Form(...),
    link_venda: str = Form(...),
    descricao: str = Form(...),
    db: Session = Depends(get_db)
):
    # Lógica para criar o slug: "Nexus Mines" vira "nexus-mines"
    slug_gerado = re.sub(r'\W+', '-', nome.lower()).strip('-')
    
    novo_produto = models.Produto(
        nome=nome,
        slug=slug_gerado,
        tipo=tipo,
        categoria=categoria_txt,
        preco=preco,
        imagem_url=imagem_url,
        link_venda=link_venda,
        descricao=descricao
    )
    
    try:
        db.add(novo_produto)
        db.commit()
        return RedirectResponse(url="/produtos", status_code=303)
    except Exception as e:
        db.rollback()
        # Se o slug já existir, dará erro de integridade (unique constraint)
        raise HTTPException(status_code=400, detail="Erro: Este nome de produto já existe no sistema.")
