from sqlalchemy.orm import Session
from core.security import get_password_hash
from app.models import Usuario

def get_admin(session: Session):
    return session.query(Usuario).filter(Usuario.admin == True).first()

def create_admin(session: Session, email: str, password: str):
    user = Usuario(
        nome='admin',
        email=email,
        senha=get_password_hash(password),
        ativo=True,
        admin=True
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user