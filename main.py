from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import models
from database import SessionLocal, criar_banco

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

# --- ROTAS PÚBLICAS (PORTAL E MARKETPLACE) ---

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    """ Página Inicial: Lista todas as notícias por ordem de chegada """
    noticias = db.query(models.Noticia).order_by(models.Noticia.id.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "noticias": noticias})

@app.get("/post/{post_id}")
async def pagina_noticia(request: Request, post_id: int, db: Session = Depends(get_db)):
    """ Página da Notícia: Abre o conteúdo detalhado de um post """
    noticia = db.query(models.Noticia).filter(models.Noticia.id == post_id).first()
    
    if not noticia:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    
    return templates.TemplateResponse("post.html", {"request": request, "noticia": noticia})

@app.get("/produtos")
async def pagina_produtos(request: Request, db: Session = Depends(get_db)):
    """ 
    Marketplace Inteligente/A: 
    Busca os itens e envia com a chave 'produtos' para o seu novo HTML 
    """
    lista_db = db.query(models.Produto).all()
    # Enviamos como "produtos" para bater com o {% for p in produtos %}
    return templates.TemplateResponse("produtos.html", {"request": request, "produtos": lista_db})

# --- SISTEMA DE ACESSO AOS ROBÔS (VIP) ---

@app.get("/app/acesso/{robo_slug}")
async def login_robo_page(request: Request, robo_slug: str):
    """ Exibe a tela de login para um robô específico """
    return templates.TemplateResponse("robo_vip.html", {
        "request": request, 
        "slug": robo_slug
    })

@app.post("/app/validar/{robo_slug}")
async def validar_acesso(request: Request, robo_slug: str, chave: str = Form(...)):
    """ Valida a chave e libera o painel do robô """
    CHAVE_ATUAL = "VIP2026_FEV" 
    
    if chave == CHAVE_ATUAL:
        # Carrega o painel interno da pasta templates/paineis/
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
    """ Painel administrativo simples """
    return templates.TemplateResponse("admin.html", {"request": request})

@app.post("/admin/postar")
async def salvar_noticia(
    titulo: str = Form(...), 
    categoria: str = Form(...), 
    conteudo: str = Form(...), 
    imagem_url: str = Form(...),
    db: Session = Depends(get_db)
):
    """ Salva uma nova notícia no banco de dados e volta para a Home """
    nova_noticia = models.Noticia(
        titulo=titulo,
        categoria=categoria,
        conteudo=conteudo,
        imagem_url=imagem_url
    )
    db.add(nova_noticia)
    db.commit()
    # Redireciona para evitar reenvio de formulário ao atualizar a página
    return RedirectResponse(url="/", status_code=303)
