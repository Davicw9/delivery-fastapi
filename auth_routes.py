from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from schemas import UsuarioSchema
from sqlalchemy.orm import session
from dependencies import pegar_sessao
from main import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/login")
async def home():
    """Rota padrão de autenticação de usuários do nosso sistema."""
    return {"message": "Você acessou a rota padrão de autenticação", "autenticação": False}


@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: session=Depends(pegar_sessao)):
    """Rota para criar uma nova conta de usuário."""
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="E-mail de usuário jo existe")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"message": f"Novo usuario cadastrado com sucesso {usuario_schema.email}"}
