from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

    class config:
        from_attributes = True

class PedidoSchema(BaseModel):
    id_usuario: int

    class config:
        from_attributes = True