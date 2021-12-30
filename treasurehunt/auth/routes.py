from fastapi import APIRouter, Body, Depends, HTTPException, status

from treasurehunt.auth.exceptions import AuthException
from treasurehunt.auth.handlers import AUTH_HANDLER
from treasurehunt.auth.repository import (
    get_in_memory_auth_repository_singleton,
)
from treasurehunt.auth.schemas import APIAuthIn, APIPostLoginOut, AuthDetails

auth_router = APIRouter()


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    auth_repo=Depends(get_in_memory_auth_repository_singleton),
    auth_in: APIAuthIn = Body(...),
):
    hashed_password = AUTH_HANDLER.get_password_hash(auth_in.password)
    try:
        await auth_repo.create_user(
            AuthDetails(user_id=auth_in.username, hash=hashed_password)
        )
    except AuthException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username is taken"
        )
    return


@auth_router.post(
    "/login",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=APIPostLoginOut,
)
async def login(
    auth_repo=Depends(get_in_memory_auth_repository_singleton),
    auth_in: APIAuthIn = Body(...),
):
    user = await auth_repo.read_user(user_id=auth_in.username)
    if (user is None) or (
        not AUTH_HANDLER.verify_password(auth_in.password, user.hash)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username and/or password",
        )
    token = AUTH_HANDLER.encode_token(user.hash)
    return APIPostLoginOut(token=token)
