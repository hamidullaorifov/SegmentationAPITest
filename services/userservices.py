# from sqlalchemy.orm import Session
# from app.db import models
# from app.schemas import users
# from app.services.auth import get_password_hash, verify_password

# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()

# def create_user(db: Session, user: users.UserCreate):
#     hashed_password = get_password_hash(user.password)
#     db_user = models.User(username=user.username, email=user.email, password=hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user



