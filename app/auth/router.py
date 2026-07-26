import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import Token, AdminResponse
from app.auth.security import create_access_token, revoke_token
from app.auth.dependency import get_current_admin, oauth2_scheme

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=Token,
    summary="Admin Login",
)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate the admin with username & password.
    Returns a JWT access token.

    Uses OAuth2PasswordRequestForm so the Swagger /docs
    "Authorize" button works out of the box.
    """

    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if (
        form_data.username != admin_username
        or form_data.password != admin_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        {"sub": form_data.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post(
    "/logout",
    summary="Admin Logout",
)
def logout(
    token: str = Depends(oauth2_scheme),
    _current_admin: dict = Depends(get_current_admin),
):
    """
    Logout the current admin by revoking their token.
    The token will no longer be accepted for future requests.
    """

    revoke_token(token)

    return {"message": "Successfully logged out."}


@router.get(
    "/me",
    response_model=AdminResponse,
    summary="Current Admin Info",
)
def get_me(
    current_admin: dict = Depends(get_current_admin),
):
    """Return the currently authenticated admin's info."""

    return current_admin