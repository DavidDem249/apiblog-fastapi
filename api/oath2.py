from datetime import datetime, timedelta, timezone
from typing import Dict, Union
from jose import jwt, JWTError
from dotenv import load_dotenv
from pathlib import Path
from .schemas import TokenData, db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


import os

# Chargement des variables d'environnement
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Valeur par défaut
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))  # 30 min par défaut


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: Dict[str, Union[str, int]]) -> str:
    """
    Crée un token JWT avec expiration
    Args:
        data: Données à encoder dans le token
    Returns:
        str: Token JWT encodé
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token

# def verify_access_token(token: str, credential_exception):
#     try:
#         payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])

#         id: str = payload.get("id")

#         if not id:
#             raise credential_exception
        
#         token_data = TokenData(id=id)
#         return token_data
#     except JWTError:
#         raise credential_exception

def verify_access_token(token: str, credential_exception: Dict):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # id: str = payload.get("id")
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credential_exception
        token_data = TokenData(id=user_id)
        return token_data  # Conversion en ObjectId
    except JWTError:
        raise credential_exception



async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not verify token, token expired",
        headers={"WWW-AUTHENTICATE": "Bearer", }
    )

    current_user_id = verify_access_token(token=token, credential_exception=credential_exception).id

    current_user = await db["users"].find_one({"_id": current_user_id})

    return current_user