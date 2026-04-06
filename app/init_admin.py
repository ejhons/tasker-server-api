import os
from sqlalchemy.orm import Session
from app.crud import get_admin, create_admin

def create_admin_if_not_exists(session:Session):
    admin = get_admin(session)

    if not admin:
        email = os.getenv("ADMIN_EMAIL", "admin@admin.com")
        password = os.getenv("ADMIN_PASSWORD", "admin123")

        print("Criando usuário admin padrão...")

        create_admin(session, email, password)