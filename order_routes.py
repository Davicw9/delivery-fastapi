from fastapi import APIRouter

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def pedidos():
    """Rota padrão de pedidos do nosso sistema. Todas as rotas relacionadas a pedidos precisam de autenticação."""
    return {"message": "Você acessou a rota de pedidos"}