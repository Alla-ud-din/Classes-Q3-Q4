from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import Session, select
from todo_app.main import get_session
from todo_app.models import Refresh_TokenData, TokenData, User
from jose import jwt, JWTError

SECRET_KEY = 'fb5d7c90c8a52dfade25191500dd2091227a342d8acf92933f7aabd40f723a3f'
ALGORITHYM = "HS256"
EXPIRY_TIME = 1 

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/token") 

pwd_context = CryptContext(schemes="bcrypt")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password):
    return pwd_context.verify(password, hash_password)

def get_user_from_db(session: Annotated[Session, Depends(get_session)], username: str, email: str):
    statement = select(User).where(User.username == username)
    session.exec(statement).first()
    if not user:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        if user:
            return user
    return user

def authenticate_user(username, email, password,  session:Annotated[Session, Depends(get_session)]):
    db_user = get_user_from_db(session, username = username, email = email)
    if not db_user:
        return False
    if not verify_password(password=password, hash_password= db_user.password):
        return False
    return db_user

def create_access_token(data: dict, expiry_time: timedelta | None):
    data_to_encode = data.copy()
    if expiry_time:
        expire = datetime.now(timezone.utc) + expiry_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = 15)
    data_to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(data_to_encode,  SECRET_KEY, algorithm= ALGORITHYM)
    return encoded_jwt

def current_user(token:Annotated[str, Depends(oauth_scheme)], session:Annotated[Session, Depends(get_session)]):
    credential_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token, Please login again",
        headers={"www-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHYM)
        username : str | None = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data =  TokenData(username=username)
    except:
        raise JWTError
    user = get_user_from_db(session, username = token_data.username)
    if not user:
        raise credential_exception
    return user

def create_refresh_token(data: dict, expiry_time: timedelta | None):
    data_to_encode = data.copy()
    if expiry_time:
        expire = datetime.now(timezone.utc) + expiry_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = 15)
    data_to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(data_to_encode,  SECRET_KEY, algorithm= ALGORITHYM)
    return encoded_jwt

def validate_refresh_token (token:str,
                            session:Annotated[Session, Depends(get_session)]):
    
    credential_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token, Please login again",
        headers={"www-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHYM)
        email : str | None = payload.get("sub")
        if email is None:
            raise credential_exception
        token_data =  Refresh_TokenData(email=email)
    except:
        raise JWTError
    user = get_user_from_db(session, email = token_data.email)
    if not user:
        raise credential_exception
    return user