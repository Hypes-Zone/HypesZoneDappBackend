from sqlalchemy.orm import Session

from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from authentication.services.JWTService import JWTService
from db.connector import get_db
from user.services import user_session_services

import jwt
from fastapi import HTTPException

security = HTTPBearer()

def verify_jwt(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    token = credentials.credentials  # Extract token

    try:
        # Decode JWT partially to get the public_key field
        unverified_payload = jwt.decode(token, options={"verify_signature": False})
        public_key = unverified_payload.get("public_key")

        if not public_key:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing public_key in token")

        # Get user session
        user_session = user_session_services.get_user_session_if_exists(public_key=public_key, db=db)
        if not user_session:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        # Retrieve partial secret from database
        jwt_service = JWTService(public_key=public_key, user_session=user_session, db=db)
        if jwt_service.is_jwt_token_expired(jwt_token=token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return jwt_service.jwt_verified_payload  # Return decoded token payload

    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
