from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import models
from database import SessionLocal, criar_banco

app = FastAPI()

# Inicializa o banco com as novas colunas (slug, categoria, etc.) [cite: 2026-01-31]
criar_banco()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROTAS PÚBLICAS (PORTAL E LOJA) ---

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    # Puxa as notícias para o index.html [cite: 2026-02-15]
    noticias = db.query(models.Noticia).order_by(models.Noticia.id.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "noticias": noticias})

# NOVA ROTA: ESSA É A QUE ESTAVA FALTANDO PARA O "LER MAIS" FUNCIONAR [cite: 2026-02-05]
@app.get("/post/{post_id}")
async def pagina_noticia(request: Request, post_id: int, db: Session = Depends(get_db)):
    # Busca a notícia específica pelo ID que veio do clique no HTML [cite: 2026-02-15]
    noticia = db.query(models.Noticia).filter(models.Noticia.id == post_id).first()
    
    if not noticia:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    
    # Renderiza o arquivo post.html que vi na sua pasta templates [cite: 2026-01-31]
    return templates.TemplateResponse("post.html", {"request": request, "noticia": noticia})

@app.get("/produtos")
async def pagina_produtos(request: Request, db: Session = Depends(get_db)):
    lista_produtos = db.query(models.Produto).all()
    return templates.TemplateResponse("produtos.html", {"request": request, "produtos": lista_produtos})

# --- SISTEMA DE ACESSO DINÂMICO AOS ROBÔS ---

@app.get("/app/acesso/{robo_slug}")
async def login_robo_page(request: Request, robo_slug: str):
    return templates.TemplateResponse("robo_vip.html", {
        "request": request, 
        "slug": robo_slug
    })

@app.post("/app/validar/{robo_slug}")
async def validar_acesso(request: Request, robo_slug: str, chave: str = Form(...)):
    CHAVE_ATUAL = "VIP2026_FEV" 
    
    if chave == CHAVE_ATUAL:
        # Tenta carregar o painel específico na pasta templates/paineis/ [cite: 2026-01-31]
        return templates.TemplateResponse(f"paineis/{robo_slug}.html", {"request": request})
    else:
        return templates.TemplateResponse("robo_vip.html", {
            "request": request, 
            "slug": robo_slug,
            "erro": "❌ Chave inválida ou expirada para este mês."
        })

# --- ADMINISTRAÇÃO ---

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
        titulo=titulo,
        categoria=categoria,
        conteudo=conteudo,
        imagem_url=imagem_url
    )
    db.add(nova_noticia)
    db.commit()
    return RedirectResponse(url="/", status_code=303)
