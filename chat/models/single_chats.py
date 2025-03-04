import uuid
from datetime import datetime

from db.connector import Base
from sqlalchemy import Column, Integer, Boolean, String


class SingleChatModel(Base):
    __tablename__ = "singlechats"

    # Room ID
    room_id = Column(String, primary_key=True, nullable=False, unique=True, index=True, default=str(uuid.uuid4()))

    # User Initiator
    public_key_user_initiator = Column(String, primary_key=True, nullable=False)

    # User Receiver
    public_key_user_receiver = Column(String, primary_key=True, nullable=False)

    # Created At
    created_at = Column(String, server_default=datetime.now().strftime("%m-%d-%Y %H:%M:%S"))

    # Chat accepted True/False
    chat_accepted = Column(Boolean, nullable=True)
