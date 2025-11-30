from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/login")
async def autenticar():
    """Rota padrão de autenticação de usuários do nosso sistema."""
    return {"message": "Você acessou a rota padrão de autenticação", "autenticação": False}