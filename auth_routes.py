from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import session
from dependencies import pegar_sessao
from main import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario):
    """Função para criar token JWT (a ser implementada)."""
    token = f"adf5sa4f2d1agwfags{id_usuario}"
    return token

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

# login - email e senha -> token JWT (Jason Web Token) nbbvmdsa564df621sc98easd4fw6a
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: session=Depends(pegar_sessao)):
    """Rota para autenticação de usuários e geração de token JWT."""
    usuario = session.query(Usuario).filter(Usuario.email == login_schema.email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não encontrado")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "bearer"
            }