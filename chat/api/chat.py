from fastapi import APIRouter, Depends, status, HTTPException, WebSocket, security

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


class Room:
    def __init__(self, room_id):
        self.room = room_id
        self.connections = []

    async def broadcast(self, message, sender):
        for connection in self.connections:
            print(message)
            await connection.send_text(message)

room_dict = {}


@chat_routers.websocket('/ws/{room_id}/{public_key}/{jwt_token}')
async def websocket_endpoint(
        websocket: WebSocket,
        room_id: str,
        public_key: str,
        jwt_token: str,
        db: Session = Depends(get_db)
):
    # Manually create HTTPAuthorizationCredentials
    credentials = security.HTTPAuthorizationCredentials(scheme="Bearer", credentials=jwt_token)

    # Verify JWT
    verified_payload = verify_jwt(credentials, db)
    if not verified_payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JWT")

    # Verify if the user is part of the chat room
    user_session = user_session_services.get_user_session_if_exists(public_key=verified_payload["public_key"], db=db)
    if not user_session:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not part of the chat room")


    try:
        await websocket.accept()

        if room_id not in room_dict:
            room_dict[room_id] = Room(room_id)

        room = room_dict[room_id]
        room.connections.append(websocket)

        print(f"connection established for {public_key} in room {room_id}")

        while True:
            data = await websocket.receive_text()
            await room.broadcast(data, websocket)
    except Exception as e:
        if room_id not in room_dict:
            room = room_dict[room_id]
            room.connections.remove(websocket)
            if len(room.connections) == 0:
                del room_dict[room_id]
