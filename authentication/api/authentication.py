
from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session

from authentication.services.JWTService import JWTService
from authentication.services.web3authService import Web3AuthService
from db.connector import get_db

from user.services import user_services, user_session_services

authentication_routers = APIRouter()

MESSAGE = """
    In order to authenticate with your wallet we need you to sign the following message:
    "Hypes Zone": XXX"""


@authentication_routers.post("/api/v1/csrf-message/", tags=["auth"])
async def get_csrf_message(data: dict, db: Session = Depends(get_db)):
    """
    Get or Create a
    :param data:
    :param db:
    :return:
    """
    public_key = data["public_key"]
    if not public_key:
        return {"message": "Public Key is required"}

    # Get or Create a User
    user_services.get_or_create_user(public_key=public_key, db=db)

    # Get or Create a User Session
    user_session = user_session_services.get_or_create_user_session(public_key=public_key, db=db)
    user_session = user_session_services.get_new_csrf_user_session(user_session=user_session, db=db)

    message = MESSAGE.replace("XXX", str(user_session.csrf_token))
    return {"message": message}


@authentication_routers.post("/api/v1/sign-in/", tags=["auth"])
async def sign_in(data: dict, db: Session = Depends(get_db)):
    """
    Sign In
    :param data:
    :param db:
    :return:
    """
    signature = data["signature"]
    public_key = data["public_key"]

    # Get user session
    user_session = user_session_services.get_user_session_if_exists(public_key=public_key, db=db)
    if not user_session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    web3_auth_service = Web3AuthService(
        public_key=public_key,
        signature=signature,
        original_message=MESSAGE,
        db=db
    )

    # Verify the signed message
    signature_verified = web3_auth_service.verify_signed_message()
    if not signature_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Get a JWT token
    jwt_service = JWTService(public_key=public_key, user_session=user_session, db=db)
    jwt_token = jwt_service.get_new_jwt_token()
    return {"jwt": jwt_token}

