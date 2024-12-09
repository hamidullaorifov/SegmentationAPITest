# from datetime import timedelta, datetime

# from passlib.context import CryptContext
# from jose import JWTError, jwt
# from sqlalchemy.orm import Session

# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer


# from app.db.setup import get_db
# from app.core import config
# from app.services import userservices

# SECRET_KEY = config.SECRET_KEY
# ALGORITHM = config.ALGORITHM
# ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now() + expires_delta
#     else:
#         expire = datetime.now() + timedelta(minutes=30)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if not email:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = userservices.get_user_by_email(db, email=email)
#     if user is None:
#         raise credentials_exception
#     return user


# def authenticate_user(db: Session, email: str, password: str):
#     user = userservices.get_user_by_email(db, email)
#     if not user:
#         return False
#     if not verify_password(password, user.password):
#         return False
#     return user