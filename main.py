from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import models
from database import SessionLocal, criar_banco
import re

app = FastAPI()

# 1. Inicializa o banco (Garante que as tabelas existam)
criar_banco()

# 2. Configurações de arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 3. Dependência para conexão com o banco
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
    produtos = db.query(models.Produto).all()
    return templates.TemplateResponse("produtos.html", {"request": request, "produtos": produtos})

# --- ADMINISTRAÇÃO ---

@app.get("/admin")
async def pagina_admin(request: Request):
    """ Exibe o painel administrativo """
    return templates.TemplateResponse("admin.html", {"request": request})

# 1. Rota para Salvar Notícia
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
    return RedirectResponse(url="/admin", status_code=303)

# 2. Rota para Salvar Produto (Com múltiplos links)
@app.post("/admin/cadastrar_produto")
async def salvar_produto(
    nome: str = Form(...),
    tipo: str = Form(...),
    categoria_txt: str = Form(...),
    preco: str = Form(None),
    imagem_url: str = Form(...),
    link_venda: str = Form(...),      # Link 1
    link_venda_2: str = Form(None),   # Link 2 (opcional)
    link_venda_3: str = Form(None),   # Link 3 (opcional)
    descricao: str = Form(...),
    db: Session = Depends(get_db)
):
    slug_gerado = re.sub(r'\W+', '-', nome.lower()).strip('-')
    
    novo_produto = models.Produto(
        nome=nome,
        slug=slug_gerado,
        tipo=tipo,
        categoria=categoria_txt,
        preco=preco,
        imagem_url=imagem_url,
        link_venda=link_venda,
        link_venda_2=link_venda_2,
        link_venda_3=link_venda_3,
        descricao=descricao
    )
    
    try:
        db.add(novo_produto)
        db.commit()
        return RedirectResponse(url="/admin", status_code=303)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro ao cadastrar: Nome ou Slug duplicado.")

# --- ROTAS DE EXCLUSÃO (GERENCIAMENTO) ---

@app.get("/admin/excluir/noticia/")
async def excluir_noticia(id: int, db: Session = Depends(get_db)):
    """ Exclui uma notícia pelo ID """
    item = db.query(models.Noticia).filter(models.Noticia.id == id).first()
    if item:
        db.delete(item)
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@app.get("/admin/excluir/produto/")
async def excluir_produto(id: int, db: Session = Depends(get_db)):
    """ Exclui um produto pelo ID """
    item = db.query(models.Produto).filter(models.Produto.id == id).first()
    if item:
        db.delete(item)
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)
