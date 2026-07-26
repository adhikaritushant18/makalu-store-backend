from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.auth.security import verify_access_token

# This tells FastAPI (and Swagger UI) where the login endpoint is,
# so the "Authorize" button in /docs works automatically.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_admin(
    token: str = Depends(oauth2_scheme),
) -> dict:
    """
    Dependency that extracts and validates the JWT from the
    Authorization: Bearer <token> header.

    Returns the decoded payload (contains "sub" = username).
    Raises 401 if the token is missing, expired, or revoked.
    """

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username: str = payload.get("sub")

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"username": username}