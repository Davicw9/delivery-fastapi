from fastapi import Depends, HTTPException
from main import ALGORITHM, SECRET_KEY, oauth2_schema
from models import Usuario
from jose import JWTError, jwt
from models import db
from sqlalchemy.orm import sessionmaker, Session

def pegar_sessao():
    """Dependência para obter uma sessão do banco de dados."""
    
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_schema), session: Session=Depends(pegar_sessao)):
    """Função para verificar token JWT e obter o usuário associado."""
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError as error:
        print(error)
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return usuario