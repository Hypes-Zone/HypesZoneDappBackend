from fastapi import APIRouter, Depends, status, HTTPException
from solders.solders import Pubkey
from sqlalchemy.orm import Session

from authentication.api.helpers.jwt_authentication import verify_jwt
from chat.schemas.single_chats_schema import SingleChat
from chat.services.chat_services import create_single_chat_if_none_exists, get_all_initiator_single_chats, \
    get_all_receiver_single_chats

from user.services import user_services, user_session_services

from db.connector import get_db

chat_routers = APIRouter()


@chat_routers.post("/api/v1/create-new-singe-chat/", tags=["auth"])
async def create_new_single_chat(
        verified_payload: dict = Depends(verify_jwt),
        data: SingleChat = None,
        db: Session = Depends(get_db)
):
    """
    Create a new Single Chat
    """
    # Verify if public_key_receiver exists as a user
    user = user_services.get_user_if_exists(public_key=data.public_key_initiator, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    public_key_receiver = data.public_key_receiver
    pub_key_receiver = Pubkey.from_string(public_key_receiver)
    if not pub_key_receiver.is_on_curve():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid public key")

    try:
        single_chat, new_chat = create_single_chat_if_none_exists(
            public_key_initiator=data.public_key_initiator, public_key_receiver=data.public_key_receiver, db=db
        )
        return {
            "single_chat": single_chat,
            "new_chat": new_chat
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@chat_routers.get("/api/v1/get-chat-rooms/", tags=["auth"])
async def get_chat_rooms(
        verified_payload: dict = Depends(verify_jwt),
        db: Session = Depends(get_db),
        public_key: str = None
):
    """
    Get all chat rooms
    """
    pub_key = Pubkey.from_string(public_key)
    if not pub_key.is_on_curve():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid public key")


    result = get_all_initiator_single_chats(public_key=public_key, db=db)
    result = result + get_all_receiver_single_chats(public_key=public_key, db=db)

    return {"chat_rooms": result}
