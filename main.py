from fastapi import FastAPI, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import models
from database import SessionLocal, criar_banco

app = FastAPI()

# Inicializa o banco com as novas colunas (slug, categoria, etc.)
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
    noticias = db.query(models.Noticia).order_by(models.Noticia.data_criacao.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "noticias": noticias})

@app.get("/produtos")
async def pagina_produtos(request: Request, db: Session = Depends(get_db)):
    # Busca todos os produtos para a loja organizada por colunas no HTML
    lista_produtos = db.query(models.Produto).all()
    return templates.TemplateResponse("produtos.html", {"request": request, "produtos": lista_produtos})

# --- SISTEMA DE ACESSO DINÂMICO AOS ROBÔS ---

# 1. Página de Login Individual (ex: /app/acesso/mines)
@app.get("/app/acesso/{robo_slug}")
async def login_robo_page(request: Request, robo_slug: str):
    return templates.TemplateResponse("robo_vip.html", {
        "request": request, 
        "slug": robo_slug
    })

# 2. Validação da Chave Mensal
@app.post("/app/validar/{robo_slug}")
async def validar_acesso(request: Request, robo_slug: str, chave: str = Form(...)):
    # CHAVE DO MÊS: Você pode mudar aqui todo final de mês
    CHAVE_ATUAL = "VIP2026_FEV" 
    
    if chave == CHAVE_ATUAL:
        # Se a chave estiver certa, renderiza o painel específico do robô
        # O arquivo deve estar em templates/paineis/nome-do-robo.html
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