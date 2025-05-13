from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated

from ..schemas import db
from .. import utils
from ..oath2 import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

# Modèle pour la réponse du token
class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Authentification OAuth2 avec username/password
    Retourne un token JWT valide
    """
    # Recherche de l'utilisateur
    user = await db['users'].find_one({"name": form_data.username})
    
    # Vérification des credentials
    if not user or not utils.verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Création du token
    access_token = create_access_token({"sub": str(user["_id"])})
    
    return {"access_token": access_token, "token_type": "bearer"}