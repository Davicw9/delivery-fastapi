from fastapi import APIRouter, Depends
from sqlalchemy.orm import session
from dependencies import pegar_sessao
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def pedidos():
    """Rota padrão de pedidos do nosso sistema. Todas as rotas relacionadas a pedidos precisam de autenticação."""
    return {"message": "Você acessou a rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: session=Depends(pegar_sessao)):
    """Rota para criar um novo pedido no sistema."""
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"message": f"Pedido criado com sucesso! {novo_pedido.id}"}