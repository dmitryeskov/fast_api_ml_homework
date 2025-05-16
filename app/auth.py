import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Auth:
    def __init__(self, db: dict):
        self.secret_key = os.environ.get("SECRET_KEY", "my_secret_key")
        self.algorithm = os.environ.get("ALGORITHM", "HS256")
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.db = db

    def get_password_has(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_pasword(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, username: str, password: str, db: dict) -> bool:
        user = db.get(username)
        if not user or not self.verify_pasword(password, user["hashed_password"]):
            return None
        return user

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        expire = (
            datetime.utcnow() + expires_delta
            if expires_delta
            else datetime.utcnow() + timedelta(minutes=15)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user name or password",
            headers={"WWW-Authentificate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username = payload.get("sub")
            if username is None:
                raise credential_exception

            token_data = TokenData(username=username)
        except jwt.PyJWTError:
            raise credential_exception

        user: dict = self.db.get(token_data.username)
        if user is None:
            raise credential_exception

        user.pop("hashed_password")
        return user
