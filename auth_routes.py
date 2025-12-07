from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import session
from dependencies import pegar_sessao
from main import bcrypt_context, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

#------------------- Funções auxiliares ------------------#

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    """Função para criar token JWT"""
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": id_usuario, "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado

def autenticar_usuario(email, senha, session):
    """Função para autenticar usuário"""
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

def verificar_token(token, session: session=Depends(pegar_sessao)):
    return usuario.session.query(Usuario).filter(Usuario.id == 1).first()

#------------------- Rotas de autenticação ------------------#

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

# login - email e senha -> token JWT (Jason Web Token) nbbvmdsa564df621sc98easd4fw6a
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: session=Depends(pegar_sessao)):
    """Rota para autenticação de usuários e geração de token JWT."""
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não encontrado ou senha incorreta")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
            }
    
@auth_router.post("/refresh")
async def refresh_token(token):
    """Rota para refresh token (atualização do token de acesso)."""
    usuario = verificar_token(token)
    access_token = criar_token()
    return {
            "access_token": access_token,
            "token_type": "bearer"
            }