import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.auth.service import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login",
)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:

    print("TOKEN RECEIVED:", token)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    try:
        payload = decode_access_token(token)

        print("JWT PAYLOAD:", payload)

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user = db.get(User, int(user_id))

        print("USER FOUND:", user)

    except (ValueError, TypeError, jwt.InvalidTokenError) as exc:
        print("JWT ERROR:", repr(exc))
        raise credentials_exception

    if user is None:
        raise credentials_exception

    return user