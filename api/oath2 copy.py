from jose import JOSEError, jwt
from datetime import date, datetime, timedelta, timezone
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict

import os

env_path = Path(__file__).parent / ".env"  # __file__ = emplacement de send_email.py
load_dotenv(env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(payload: Dict):
    to_encode = payload.copy()

    # expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiration_time})

    jwt_token = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token